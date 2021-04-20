from abc import abstractmethod, ABCMeta


class Layer(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.weights = self.bias = None

    @abstractmethod
    def forward(self, inp):
        raise NotImplementedError

    @abstractmethod
    def backward(self, inp, lr):
        raise NotImplementedError


class Activation(metaclass=ABCMeta):
    @abstractmethod
    def forward(self, inp):
        raise NotImplementedError

    @abstractmethod
    def backward(self, inp, lr):
        raise NotImplementedError
