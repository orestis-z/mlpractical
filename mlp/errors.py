# -*- coding: utf-8 -*-
"""Error functions.

This module defines error functions, with the aim of model training being to
minimise the error function given a set of inputs and target outputs.

The error functions will typically measure some concept of distance between the
model outputs and target outputs, averaged over all data points in the data set
or batch.
"""

import numpy as np


class SumOfSquaredDiffsError(object):
    """Sum of squared differences (squared Euclidean distance) error."""

    def __call__(self, outputs, targets):
        """Calculates error function given a batch of outputs and targets.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Scalar cost function value.
        """
        return np.mean(np.sum((outputs - targets)**2, axis=1)) * 0.5

    def grad(self, outputs, targets):
        """Calculates gradient of error function with respect to outputs.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Gradient of error function with respect to outputs.
        """
        return (outputs - targets) / outputs.shape[0]

    def __repr__(self):
        return 'MeanSquaredErrorCost'


class BinaryCrossEntropyError(object):
    """Binary cross entropy error."""

    def __call__(self, outputs, targets):
        """Calculates error function given a batch of outputs and targets.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Scalar error function value.
        """
        return -np.mean(
            targets * np.log(outputs) + (1. - targets) * np.log(1. - ouputs))

    def grad(self, outputs, targets):
        """Calculates gradient of error function with respect to outputs.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Gradient of error function with respect to outputs.
        """
        return ((1. - targets) / (1. - outputs) -
                (targets / outputs)) / outputs.shape[0]

    def __repr__(self):
        return 'BinaryCrossEntropyError'


class BinaryCrossEntropySigmoidError(object):
    """Binary cross entropy error with logistic sigmoid applied to outputs."""

    def __call__(self, outputs, targets):
        """Calculates error function given a batch of outputs and targets.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Scalar error function value.
        """
        probs = 1. / (1. + np.exp(-outputs))
        return -np.mean(
            targets * np.log(probs) + (1. - targets) * np.log(1. - probs))

    def grad(self, outputs, targets):
        """Calculates gradient of error function with respect to outputs.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Gradient of error function with respect to outputs.
        """
        probs = 1. / (1. + np.exp(-outputs))
        return (probs - targets) / outputs.shape[0]

    def __repr__(self):
        return 'BinaryCrossEntropySigmoidError'


class CrossEntropyError(object):
    """Multi-class cross entropy error."""

    def __call__(self, outputs, targets):
        """Calculates error function given a batch of outputs and targets.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Scalar error function value.
        """
        return -np.mean(np.sum(targets * np.log(outputs), axis=1))

    def grad(self, outputs, targets):
        """Calculates gradient of error function with respect to outputs.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Gradient of error function with respect to outputs.
        """
        return -(targets / outputs) / outputs.shape[0]

    def __repr__(self):
        return 'CrossEntropyError'


class CrossEntropySoftmaxError(object):
    """Multi-class cross entropy error with Softmax applied to outputs."""

    def __init__(self, model):
        self.model = model

    def _get_weights(self):
        return np.concatenate(
            [param_layer.flatten() for param_layer in self.model.params])

    def __call__(self, outputs, targets):
        """Calculates error function given a batch of outputs and targets.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Scalar error function value.
        """

        normalized_outputs = outputs - outputs.max(-1)[:, None]
        log_prob = normalized_outputs - \
            np.log(np.sum(np.exp(normalized_outputs), axis=-1)[:, None])
        cost = -np.mean(np.sum(targets * log_prob, axis=1))
        if self.model.regularizer == 'L1':
            cost += self.model.regularizer_lambda * \
                np.linalg.norm(self._get_weights(), 1)
        elif self.model.regularizer == 'L2':
            cost += self.model.regularizer_lambda * \
                np.linalg.norm(self._get_weights(), 2)
        return cost

    def grad(self, outputs, targets):
        """Calculates gradient of error function with respect to outputs.

        Args:
            outputs: Array of model outputs of shape (batch_size, output_dim).
            targets: Array of target outputs of shape (batch_size, output_dim).

        Returns:
            Gradient of error function with respect to outputs.
        """

        probs = np.exp(outputs - outputs.max(-1)[:, None])
        probs /= probs.sum(-1)[:, None]
        return (probs - targets) / outputs.shape[0]

    def __repr__(self):
        return 'CrossEntropySoftmaxError'
