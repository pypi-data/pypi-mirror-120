# Copyright 2021, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for creating functional implementations of a `tff.learning.Model`.

This version of the model parameterizes its `forward_pass` and
`predict_on_batch` methods by model weights, rather than storing them in the
model. This allows for greater flexibility in model portability.

To use with `tff.learning.build_federated_averaging_process` and other APIs that
construct learning processes expecting stateful models, wrap the functional
model with `tff.learning.models.model_from_functional`.
"""

import collections
from typing import Any, Callable, Mapping, Sequence, Tuple, Union

import numpy as np
import tensorflow as tf

from tensorflow_federated.python.common_libs import py_typecheck
from tensorflow_federated.python.core.api import computation_base
from tensorflow_federated.python.core.api import computations
from tensorflow_federated.python.core.impl.federated_context import intrinsics
from tensorflow_federated.python.core.impl.types import computation_types
from tensorflow_federated.python.learning import model as model_lib

Weight = Union[np.ndarray, int, float]
WeightStruct = Union[Sequence[Weight], Mapping[str, Weight]]
ModelWeights = Tuple[WeightStruct, WeightStruct]


class CallableMustBeTFFunctionError(TypeError):
  """Error raised when a callable is not decorated as a tf.function."""


class ValueMustNotBeTFError(TypeError):
  """Error raised a value must not be a `tf.Tensor` or `tf.Variable`."""


class FunctionalModel():
  """A model that parameterizes forward pass by model weights."""

  def __init__(
      self,
      initial_weights: ModelWeights,
      forward_pass_fn: Callable[[ModelWeights, Any, bool],
                                model_lib.BatchOutput],
      predict_on_batch_fn: Callable[[ModelWeights, Any, bool], Any],
      input_spec,
  ):
    """Initializes a `FunctionalModel`.

    Example model implementing linear regression:

    ```
    w, b = np.zeros(shape=[1,3]), np.zeros([1])
    trainable_weights = (w, b)
    non_trainable_weights = ()
    initial_weights = (trainable_weights, non_trainable_weights)

    @tf.function
    def predict_on_batch(model_weights, x, training):
      del training  # Unused.
      trainable, non_trainable = model_weights
      w, b = trainable
      return tf.matmul(x, w, transpose_b=True) + b

    @tf.function
    def forward_pass(model_weights, batch_input, training):
      x, y = batch_input
      predictions = predict_on_batch(model_weights, , training)
      residuals = predictions - y
      total_loss = tf.reduce_sum(tf.pow(residuals, 2.))
      num_examples = tf.shape(predictions)[0]
      average_loss = total_loss / tf.cast(num_examples, tf.float32)
      return tff.learning.BatchOutput(
        loss=average_loss, predictions=predictions, num_examples=num_examples)

    model = FunctionalModel(
      initial_weights, forward_pass, predict_on_batch,
      (tf.TensorSpec(shape=[None, 3], dtype=tf.float32),
       tf.TensorSpec(shape=[None, 1], dtype=tf.float32))
    )
    ```

    Args:
      initial_weights: A 2-tuple `(trainable, non_trainable)` where the two
        elements are sequences of weights. Weights must be values convertable to
        `tf.Tensor` (e.g. `numpy.ndarray`, Python sequences, etc), but _not_
        `tf.Tensor` values.
      forward_pass_fn: A `tf.function` decorated callable that takes three
        arguments, `model_weights` the same structure as `initial_weights`,
        `batch_input` a nested structure of tensors matching `input_spec`, and
        `training` a boolean determinig whether the call is during a training
        pass (e.g. for Dropout, BatchNormalization, etc).
      predict_on_batch_fn: A `tf.function` decorated callable that takes three
        arguments, `model_weights` the same structure as `initial_weights`, `x`
        the first element of `batch_input` (or `input_spec`), and `training` a
        boolean determinig whether the call is during a training pass (e.g. for
        Dropout, BatchNormalization, etc).
      input_spec: A 2-tuple of `(x, y)` where each element is a nested structure
        of `tf.TensorSpec` that defines the shape and dtypes of `batch_input` to
        `forward_pass_fn`. `x` corresponds to batched model inputs and `y`
        corresponds to batched labels for those inputs.
    """

    def check_tf_function_decorated(fn, arg_name):
      if not hasattr(fn, 'get_concrete_function'):
        type_string = py_typecheck.type_string(type(fn))
        raise CallableMustBeTFFunctionError(
            f'{arg_name} does not have a `get_concrete_function` attribute '
            'meaning it is not a callable decorated with `tf.function`. '
            f'Got a {type_string} with value {fn!r}.')

    def check_non_tf_value(value):
      if tf.is_tensor(value) or isinstance(value, tf.Variable):
        raise ValueMustNotBeTFError(
            'initial_weights may not contain TensorFlow values '
            f'(tf.Tensor or tf.Variable). Got: {type(value)!r}. Try '
            'converting to a np.ndarray by using the `.numpy()` '
            'attribute for tf.Tensor, or `.read_value().numpy()` '
            'for tf.Variable.')

    tf.nest.map_structure(check_non_tf_value, initial_weights)
    self._initial_weights = initial_weights
    check_tf_function_decorated(forward_pass_fn, 'forward_pass_fn')
    self._forward_pass_fn = forward_pass_fn
    check_tf_function_decorated(predict_on_batch_fn, 'predict_on_batch_fn')
    self._predict_on_batch_fn = predict_on_batch_fn
    self._input_spec = input_spec

  @property
  def initial_weights(self) -> ModelWeights:
    return self._initial_weights

  @tf.function
  def forward_pass(self,
                   model_weights: ModelWeights,
                   batch_input: Any,
                   training: bool = True) -> model_lib.BatchOutput:
    """Runs the forward pass and returns results."""
    return self._forward_pass_fn(model_weights, batch_input, training)

  @tf.function
  def predict_on_batch(self,
                       model_weights: ModelWeights,
                       x: Any,
                       training: bool = True):
    """Returns tensor(s) interpretable by the loss function."""
    return self._predict_on_batch_fn(model_weights, x, training)

  @property
  def input_spec(self):
    return self._input_spec


class _ModelFromFunctional(model_lib.Model):
  """A `tff.learning.Model` wrapping a `tff.learning.model.FunctionalModel`."""

  def __init__(self, functional_model: FunctionalModel):
    self._functional_model = functional_model
    # Construct `tf.Variable` to optimize during the learning process.
    trainable, non_trainable = functional_model.initial_weights
    self._trainable_variables = tuple(tf.Variable(x) for x in trainable)
    self._non_trainable_variables = tuple(
        tf.Variable(x, trainable=False) for x in non_trainable)
    self._model_weights = (self._trainable_variables,
                           self._non_trainable_variables)
    self._num_examples = tf.Variable(0, trainable=False)
    self._loss_sum = tf.Variable(0.0, trainable=False)

  @property
  def trainable_variables(self) -> Tuple[tf.Variable, ...]:
    return self._trainable_variables

  @property
  def non_trainable_variables(self) -> Tuple[tf.Variable, ...]:
    return self._non_trainable_variables

  @property
  def local_variables(self) -> Tuple[tf.Variable, ...]:
    return (self._loss_sum, self._num_examples)

  @property
  def input_spec(self):
    return self._functional_model.input_spec

  @tf.function
  def forward_pass(self, batch_input, training=True):
    batch_output = self._functional_model.forward_pass(
        model_weights=tf.nest.map_structure(lambda v: v.read_value(),
                                            self._model_weights),
        batch_input=batch_input,
        training=training)
    self._num_examples.assign_add(batch_output.num_examples)
    self._loss_sum.assign_add(batch_output.loss *
                              tf.cast(batch_output.num_examples, tf.float32))
    return batch_output

  @tf.function
  def predict_on_batch(self, x, training=True):
    return self._functional_model.predict_on_batch(
        model_weights=tf.nest.map_structure(lambda v: v.read_value(),
                                            self._model_weights),
        x=x,
        training=training)

  @tf.function
  def report_local_outputs(self):
    return collections.OrderedDict(
        loss_sum=self._loss_sum,
        num_examples=tf.cast(self._num_examples, tf.float32))

  @property
  def federated_output_computation(self) -> computation_base.Computation:

    @computations.federated_computation(
        computation_types.at_clients(
            collections.OrderedDict(
                loss_sum=tf.float32, num_examples=tf.float32)))
    def aggregate(values):
      return collections.OrderedDict(
          loss=intrinsics.federated_mean(
              values['loss_sum'], weight=values['num_examples']))

    return aggregate


def model_from_functional(functional_model: FunctionalModel) -> model_lib.Model:
  """Converts a `FunctionalModel` to a `tff.learning.Model`."""
  return _ModelFromFunctional(functional_model)
