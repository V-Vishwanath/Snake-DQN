import pygame
import random
import numpy as np
from typing import Tuple
from collections import deque

from game.core import Direction
from mlagents.model import DenseQNet
from game.snake.env import SnakeGame

pygame.init()
pygame.font.init()


MAX_MEMORY = 100_000
BATCH_SIZE = 3000


class Agent:
    @staticmethod
    def action_to_dir(curr_dir: Direction, action: Tuple[int, int, int]) -> Direction:
        dirs = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

        idx = dirs.index(curr_dir)
        direction = dirs[idx]
        if np.array_equal(action, [0, 1, 0]):
            direction = dirs[(idx + 1) % 4]  # right
        elif np.array_equal(action, [0, 0, 1]):
            direction = dirs[(idx - 1) % 4]  # left

        return direction

    def __init__(self, model=None):
        self.n_games = 0
        self.epsilon = 0

        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = DenseQNet(lr=0.001, gamma=0.9)
        if model:
            self.model.load(model)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def experience_replay(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, results = zip(*sample)
        return self.model.train_step(states, actions, rewards, next_states, results)

    def train_step(self, state, action, reward, next_state, result):
        self.model.train_step(state, [action], [reward], [next_state], [result])

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            action = [0, 0, 0]
            action[random.randint(0, 2)] = 1
            return action[0], action[1], action[2]

        return self.predict_action(state)

    def predict_action(self, state):
        action = [0, 0, 0]

        prediction = self.model.predict(state)
        move = np.argmax(prediction)

        action[move] = 1

        return action[0], action[1], action[2]


def train():
    record = 0

    display = pygame.display.set_mode((640, 480))
    env = SnakeGame(display)
    agent = Agent()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # get state and action
        state = env.get_state()
        action = agent.get_action(state)

        # perform move and get new state
        reward, game_over, score = env.step(Agent.action_to_dir(env.snake.head.direction, action))
        state_new = env.get_state()

        # train the current action
        agent.train_step(state, action, reward, state_new, game_over)
        agent.remember(state, action, reward, state_new, game_over)

        # save current model
        agent.model.save('latest_episode.pkl')

        if game_over:
            env.reset()
            agent.n_games += 1
            loss = agent.experience_replay()

            # write data to csv
            with open('losses.csv', 'a') as f:
                f.write(f'{agent.n_games},{score}\n')

            if score > record:
                record = score
                agent.model.save()

            print(f'Game: {agent.n_games} \tScore: {score} \tBest Score: {record} \tLoss: {loss}')

        env.render()
        clock.tick(30)


def play():
    display = pygame.display.set_mode((640, 480))
    env = SnakeGame(display)
    agent = Agent(model='assets/snake_agent.pkl')

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        state = env.get_state()
        action = agent.predict_action(state)
        _, game_over, _ = env.step(Agent.action_to_dir(env.snake.head.direction, action))

        if game_over:
            env.reset()

        env.render()
        clock.tick(30)


if __name__ == '__main__':
    play()
