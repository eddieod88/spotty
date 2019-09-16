import unittest
import numpy as np
import pandas as pd

from train import Train


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Data only contains the features!
        headings = ["feature_1", "feature_2"]
        with open("../data_collection/algorithm_test_data.csv", 'r') as f:
            cs_v = pd.read_csv(f, header=None)
        data = np.array(cs_v.iloc[0:, 0:2])
        self.X = pd.DataFrame(data=data, columns=headings)
        # Then add a column of ones at the start for the intercept term
        self.X.insert(0, "intercept", np.ones(len(self.X)))

        # Results need to be codified (not strings)
        result = np.array(cs_v.iloc[0:, 2])
        self.y = pd.Series(result)

        # theta needs to be the same length as the number of features (including the extra column due to the intercept)
        theta = np.ones(len(self.X.columns))
        self.theta = pd.Series(theta)

    def test_dot(self):
        # Note: theta^T . X === X^T . theta
        dot = np.dot(self.theta, self.X.T)  # need to use np dot function as pandas only allows you to do the dot if columns have same name
        print(dot)
        sig = Train._sigmoid(dot)
        print(sig)

    def test_sigmoid_scalar(self):
        # for very negative numbers, sigmoid should equal zero, for very large, it should be 1
        self.assertAlmostEqual(Train._sigmoid(-1000000), 0)
        self.assertAlmostEqual(Train._sigmoid(1000000), 1)

    def test_sigmoid_vector(self):
        small_sig = Train._sigmoid(np.array([-10000, -10000, -10000]))
        large_sig = Train._sigmoid(np.array([10000, 10000, 10000]))
        for s_val, l_val in zip(small_sig, large_sig):
            self.assertAlmostEqual(s_val, 0)
            self.assertAlmostEqual(l_val, 1)

    def test_cost_zeros(self):
        # Cost should be 0.693 when theta is zeroed
        theta_z = pd.Series(np.zeros(len(self.X.columns)))
        train = Train(self.X, self.y)
        cost = train._cost(theta_z)
        self.assertAlmostEqual(cost, 0.693, places=3)

    def test_grad(self):
        # Unsure what the grad should come to. but I think a vector of length = to number of features (+1 for intercept)
        theta_z = pd.Series(np.zeros(len(self.X.columns)))
        train = Train(self.X, self.y)
        grad = train._gradient(theta_z)
        print(grad)
        # self.assertAlmostEqual(cost, 0.693, places=3)

    def test_optimise(self):
        train = Train(self.X, self.y)
        theta_init = pd.Series(np.ones(len(self.X.columns)))
        opt = train.optimise(theta_init)
        expected_vector = np.array([-25.161, 0.206, 0.201])
        for exp_el, result_el in zip(opt, expected_vector):
            self.assertAlmostEqual(result_el, exp_el, places=3)


if __name__ == '__main__':
    unittest.main()
