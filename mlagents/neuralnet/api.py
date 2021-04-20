import pickle
import numpy as np

from mlagents.neuralnet._ABC import Layer


class NeuralNet:
    def __init__(self, layers):
        self.layers = layers
        self.loss = None

    def compile(self, loss):
        self.loss = loss

    def predict(self, inp) -> np.ndarray:
        assert len(self.layers) > 0

        if len(inp.shape) == 1:
            inp = inp[np.newaxis, ...]

        pred = inp
        for layer in self.layers:
            pred = layer.forward(pred)

        return pred

    def backward(self, loss_grad, lr=0.01):
        for layer in reversed(self.layers):
            loss_grad = layer.backward(loss_grad, lr)

    def train(self, inp, target, lr=0.01):
        assert len(self.layers) > 0 and self.loss is not None

        pred = self.predict(inp)
        loss = self.loss.calc_loss(target, pred)

        grad = self.loss.gradient(target, pred)
        self.backward(grad, lr)

        return loss

    def save(self, filename):
        weights = []
        biases = []
        for layer in self.layers:
            if isinstance(layer, Layer):
                weights.append(layer.weights)
                biases.append(layer.bias)

        with open(filename, 'wb') as f:
            pickle.dump([weights, biases], f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            weights, biases = pickle.load(f)

        index = 0
        for i in range(len(self.layers)):
            if isinstance(self.layers[i], Layer):
                self.layers[i].weights = weights[index]
                self.layers[i].bias = biases[index]
                index += 1
