import numpy as np


class MSE:
    @staticmethod
    def calc_loss(true, predicted):
        return np.mean((true - predicted) ** 2)

    @staticmethod
    def gradient(true, predicted):
        return 2 * (predicted - true) / predicted.size
