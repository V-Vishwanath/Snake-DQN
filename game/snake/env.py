import pygame
import numpy as np

from game.core import Direction, Position
from game.snake.game_objects import Snake, Food

pygame.init()
pygame.font.init()
pygame.mixer.init()


class SnakeGame:
	_COLLISION_SOUND = pygame.mixer.Sound('assets/sfx/collision.mp3')
	_FOOD_CRUNCH_SOUND = pygame.mixer.Sound('assets/sfx/apple_bite.mp3')

	_FONT = pygame.font.SysFont('arial', 18)
	_OPTIONS_TEXT = _FONT.render('ESC: MENU', True, (255, 255, 255))

	@staticmethod
	def play_bgm():
		pygame.mixer.music.load('assets/sfx/main_bgm.mp3')
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)

	def __init__(self, display: pygame.Surface):
		self.display = display
		self.win_size = display.get_size()

		self.snake = Snake(self.win_size)
		self.food = Food(self.win_size)
		self.score = self.frame_cnt = self.record = 0

	def reset(self):
		if self.score > self.record:
			self.record = self.score

		self.score = self.frame_cnt = 0
		self.snake = Snake(self.win_size)
		self.food = Food(self.win_size)

	def step(self, direction: Direction):
		self.frame_cnt += 1

		self.snake.move(direction)

		reward = 0
		game_over = False

		if self.snake.has_collision() or self.frame_cnt > 100 * len(self.snake.body):
			SnakeGame._COLLISION_SOUND.play()
			game_over = True
			reward = -10
			return reward, game_over, self.score

		if self.snake.ate(self.food):
			SnakeGame._FOOD_CRUNCH_SOUND.play()
			self.score += 1
			reward = 10

			self.snake.length += 1
			while True:
				self.food.pos = self.food.create_new()
				if not self.snake.on_body(self.food):
					break

		return reward, game_over, self.score

	def render(self):
		self.display.fill((207, 237, 154))
		pygame.draw.rect(self.display, (130, 82, 0), pygame.Rect(0, 0, 640, 480), 40)

		self.food.render(self.display)
		self.snake.render(self.display)

		score_text = SnakeGame._FONT.render(f'Score: {self.score}', True, (255, 255, 255))
		record_text = SnakeGame._FONT.render(f'Best: {self.record}', True, (255, 255, 255))

		self.display.blit(score_text, score_text.get_rect(center=(250, 10)))
		self.display.blit(record_text, record_text.get_rect(center=(390, 10)))
		self.display.blit(SnakeGame._OPTIONS_TEXT, (0, 0))

	def get_state(self):
		head_pos = self.snake.head.pos
		point_u = Position(head_pos.x, head_pos.y - 20)
		point_l = Position(head_pos.x - 20, head_pos.y)
		point_d = Position(head_pos.x, head_pos.y + 20)
		point_r = Position(head_pos.x + 20, head_pos.y)

		direction = self.snake.head.direction
		dir_u = direction == Direction.UP
		dir_l = direction == Direction.LEFT
		dir_d = direction == Direction.DOWN
		dir_r = direction == Direction.RIGHT

		head_x, head_y = head_pos
		food_x, food_y = self.food.pos

		state = [
			# Danger ahead
			(dir_r and self.snake.has_collision(point_r)) or
			(dir_l and self.snake.has_collision(point_l)) or
			(dir_u and self.snake.has_collision(point_u)) or
			(dir_d and self.snake.has_collision(point_d)),

			# Danger to right
			(dir_u and self.snake.has_collision(point_r)) or
			(dir_d and self.snake.has_collision(point_l)) or
			(dir_l and self.snake.has_collision(point_u)) or
			(dir_r and self.snake.has_collision(point_d)),

			# Danger to left
			(dir_d and self.snake.has_collision(point_r)) or
			(dir_u and self.snake.has_collision(point_l)) or
			(dir_r and self.snake.has_collision(point_u)) or
			(dir_l and self.snake.has_collision(point_d)),

			# Move direction
			dir_l, dir_r, dir_u, dir_d,

			# Food location
			food_x < head_x,  # food left
			food_x > head_x,  # food right
			food_y < head_y,  # food up
			food_y > head_y  # food down
		]

		return np.array(state, dtype=int)
