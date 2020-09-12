import numpy as np
import pandas as pd
from scipy.optimize import fmin_bfgs
from sklearn.metrics import f1_score


"""
Creating classification algo from scratch.
"""


class Classification:
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
        self.X = X  # Training dataframe
        self.y = y  # supervised predictions of trainig data - must be codified.
        self.theta = pd.Series  # Optimisation matrix
        self.m = len(y)

    def train(self, theta_init: pd.Series):
        """
            Determine the optimized value for theta such that predictions can be made on new data using the predict method.

        :param theta_init: initial values for theta
        :return: optimized theta vector which can be used in the predict method. Should perhaps store this vector in a file.
        """
        optimise = fmin_bfgs(self._cost, theta_init.values, fprime=self._gradient)
        return optimise

    def classify(self, theta_optim: pd.Series, test_X: pd.DataFrame = None):
        """
            Predict the classes of a new data set based on the optimised values of theta - if none, use the training data

        :param theta_optim: optimised theta - vector/pd.series
        :param test_X: test dataframe
        :return: a vector of the predictions
        """
        if test_X:
            X = test_X
        else:
            X = self.X
        return self._predict(np.dot(theta_optim, X.T))

    @staticmethod
    def f_score(true_vals, predicted_vals):
        """
            Method used to get a basic f_score of the model. Shows how well the predictions align with the true classifications

        :param true_vals: vector of y-values
        :param predicted_vals: vector of predictions
        :return: the f_score - a value between 0 and 1 - 1 being perfect and 0 being poor predictions (roughly speaking)
        """
        return f1_score(true_vals, predicted_vals)

    @staticmethod
    def _sigmoid(x):
        """
            This is the hypothesis function. It is used to eventually minimise theta

        :param x: vector of theta^T * X (or scalar)
        :return: Sigmoid of all of the values in the input vector
        """
        sig = 1 / (1 + np.exp(-x))
        return sig

    def _predict(self, x):
        """
        Vectorized implementation to go through the output of sig and anchor to 0 or 1 (for bin classification)

        :param x:  vector of theta^T * X (or scalar)
        :return:  prediction vector of 1's and 0's
        """
        sig = self._sigmoid(x)
        sig = pd.Series(sig)
        sig.where(sig.values >= 0.5, 0, inplace=True)  # if condition is FALSE, replace with value
        sig.where(sig.values < 0.5, 1, inplace=True)
        prediction = sig
        return prediction

    def _cost(self, theta: pd.Series):
        #  For multi-class: https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html
        cost = -(1/self.m) * (np.dot(self.y, np.log(self._sigmoid(np.dot(theta, self.X.T)))) +
                              np.dot((np.ones(len(self.y)) - self.y), np.log(np.ones(len(self.y)) -
                                                                             self._sigmoid(np.dot(theta, self.X.T)))))
        return cost

    def _gradient(self, theta: pd.Series):
        grad = (1/self.m) * np.dot(self._sigmoid(np.dot(theta, self.X.T)) - self.y, self.X)
        return grad
