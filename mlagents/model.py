import numpy as np

from mlagents.neuralnet.api import NeuralNet
from mlagents.neuralnet.layers import Dense, ReLU

from mlagents.neuralnet.losses import MSE


class DenseQNet(NeuralNet):
    def __init__(self, lr=0.01, gamma=0.9):
        super().__init__([
            Dense(11, 256),
            ReLU(),
            Dense(256, 128),
            ReLU(),
            Dense(128, 3)
        ])
        self.loss = MSE

        self.lr = lr
        self.gamma = gamma

    def save(self, filename='snake_agent.pkl'):
        super().save(filename)

    def load(self, filename='snake_agent.pkl'):
        super().load(filename)

    def train_step(self, states, actions, rewards, next_states, results):
        predicted = self.predict(np.array(states))

        target = predicted.copy()
        for idx in range(len(results)):
            q_new = rewards[idx]
            if not results[idx]:
                q_new += self.gamma * np.max(self.predict(next_states[idx]))

            target[idx][np.argmax(actions[idx])] = q_new

        return self.train(np.array(states), target, self.lr)
