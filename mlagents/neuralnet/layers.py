import numpy as np

from mlagents.neuralnet._ABC import Layer, Activation


class ReLU(Activation):
    def forward(self, inp):
        return np.maximum(inp, 0, inp)

    def backward(self, inp, lr):
        return (inp > 0) * 1.0


class Dense(Layer):
    def __init__(self, inp_size, out_size):
        super().__init__()
        scale_factor = np.sqrt(inp_size + out_size)
        self.weights = np.random.randn(inp_size, out_size) / scale_factor
        self.bias = np.random.randn(1, out_size) / scale_factor
        self.inp = None

    def forward(self, inp):
        self.inp = inp
        return np.dot(inp, self.weights) + self.bias

    def backward(self, grad_out, lr):
        inp_err = np.dot(grad_out, self.weights.T)

        self.bias = self.bias - lr * grad_out.mean(axis=0)
        self.weights = self.weights - lr * np.dot(self.inp.T, grad_out)

        return inp_err
