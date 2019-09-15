import numpy as np
import pandas as pd


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

    @staticmethod
    def _sigmoid(x):
        """
        This is the hypothesis function. It is used to eventually minimise theta
        :param x: vector of theta^T * X (or scalar)
        :return: Sigmoid of all of the values in the input vector
        """
        sig = 1 / (1 + np.exp(-x))
        print(sig)
        return sig

    def _cost(self, X: pd.DataFrame, y: pd.Series, theta: pd.Series):
        #  For multi-class: https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html
        m = len(y)
        cost = -(1/m) * (np.dot(y, np.log(self._sigmoid(np.dot(theta, X.T)))) +
                 np.dot((np.ones(len(y)) - y), np.log(np.ones(len(y)) - self._sigmoid(np.dot(theta, X.T)))))
        return cost

    def _gradient(self):
        pass
