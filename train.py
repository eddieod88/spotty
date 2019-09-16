import numpy as np
import pandas as pd
from scipy.optimize import fmin_bfgs


class Train:
    """
        Overall aim of this class is to determine the values for the vector, theta. Theta will be stored in a file
        such that it can be used for real the testing and validation data.

        Save the training data in a data frame and the tags themselves as a vector.

        Functions required:
            - Sigmoid function
            - Cost function and gradient function
            - Use fminunc using oct2py to determine theta.
    """

    def __init__(self, X: pd.DataFrame, y: pd.Series):
        self.X = X
        self.y = y
        self.theta = pd.Series

        self.m = len(y)

    @staticmethod
    def _sigmoid(x):
        """
        This is the hypothesis function. It is used to eventually minimise theta
        :param x: vector of theta^T * X (or scalar)
        :return: Sigmoid of all of the values in the input vector
        """
        sig = 1 / (1 + np.exp(-x))
        return sig

    def _cost(self, theta: pd.Series):
        #  For multi-class: https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html
        cost = -(1/self.m) * (np.dot(self.y, np.log(self._sigmoid(np.dot(theta, self.X.T)))) +
                              np.dot((np.ones(len(self.y)) - self.y), np.log(np.ones(len(self.y)) -
                                                                             self._sigmoid(np.dot(theta, self.X.T)))))
        return cost

    def _gradient(self, theta: pd.Series):
        grad = (1/self.m) * np.dot(self._sigmoid(np.dot(theta, self.X.T)) - self.y, self.X)
        return grad

    def optimise(self, theta_init: pd.Series):
        opt = fmin_bfgs(self._cost, theta_init.values, fprime=self._gradient)
        return opt
