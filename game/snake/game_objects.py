import pygame
from typing import Tuple
from random import randint
from collections import deque

from game.core import GameObject, Position, Direction


class Food(GameObject):
	_SPRITE = GameObject.load_sprite('assets/sprites/apple.png', (20, 20))

	def __init__(self, win_size: Tuple[int, int]):
		self.w, self.h = win_size
		super().__init__(pos=self.create_new(), sprite=Food._SPRITE)

	def create_new(self) -> Position:
		return Position(
			randint(2, (self.w - 40) // 20) * 20,
			randint(2, (self.h - 40) // 20) * 20
		)


class Snake:
	# load sprites
	body_parts = [GameObject.load_sprite(f'assets/sprites/snake-body/{i}.png', (20, 20)) for i in range(1, 15)]

	_HEAD_U, _HEAD_L, _HEAD_D, _HEAD_R = body_parts[0: 4]
	_TAIL_U, _TAIL_L, _TAIL_D, _TAIL_R = body_parts[4: 8]
	_TURN_UL, _TURN_UR, _TURN_DL, _TURN_DR = body_parts[8: 12]
	_BODY_H, _BODY_V = body_parts[12: 14]

	del body_parts

	class _BodyPart(GameObject):
		def __init__(self, pos: Position, direction: Direction, sprite: pygame.surface.Surface):
			self.direction = direction
			super().__init__(pos=pos, sprite=sprite)

		def copy(self):
			return Snake._BodyPart(pos=self.pos, direction=self.direction, sprite=self.sprite)

	def __init__(self, win_size: Tuple[int, int]):
		self.w, self.h = win_size

		self.head = self._BodyPart(
			pos=Position(self.w // 2, self.h // 2),
			direction=Direction.RIGHT, sprite=Snake._HEAD_R
		)

		self.body = deque([
			self.head,

			self._BodyPart(
				pos=Position(self.head.pos.x - 20, self.head.pos.y),
				direction=Direction.RIGHT, sprite=Snake._BODY_H
			),

			self._BodyPart(
				pos=Position(self.head.pos.x - 40, self.head.pos.y),
				direction=Direction.RIGHT, sprite=Snake._BODY_H
			),

			self._BodyPart(
				pos=Position(self.head.pos.x - 60, self.head.pos.y),
				direction=Direction.RIGHT, sprite=Snake._TAIL_R
			)
		])

		self.length = 4

	def move(self, direction: Direction):
		# create a new head
		head: Snake._BodyPart = self.head.copy()
		head.direction = direction
		x, y = head.pos

		if direction is Direction.UP:
			head.set_sprite(Snake._HEAD_U)
			head.pos = Position(x, y - 20)

		elif direction is Direction.LEFT:
			head.set_sprite(Snake._HEAD_L)
			head.pos = Position(x - 20, y)

		elif direction is Direction.DOWN:
			head.set_sprite(Snake._HEAD_D)
			head.pos = Position(x, y + 20)

		else:
			head.set_sprite(Snake._HEAD_R)
			head.pos = Position(x + 20, y)

		# append the new head and change the head pointer
		self.body.appendleft(head)
		self.head = head

		# remove the last body part if greater than length
		if len(self.body) > self.length:
			self.body.pop()

		# correct the sprites of the body parts (excluding the tail)
		for i in range(1, len(self.body) - 1):
			body_part = self.body[i]
			prev_body_part = self.body[i - 1]

			if prev_body_part.direction is Direction.UP:
				if body_part.direction is Direction.RIGHT: body_part.set_sprite(Snake._TURN_UR)
				elif body_part.direction is Direction.LEFT: body_part.set_sprite(Snake._TURN_UL)
				else: body_part.set_sprite(Snake._BODY_V)

			elif prev_body_part.direction is Direction.LEFT:
				if body_part.direction is Direction.UP: body_part.set_sprite(Snake._TURN_DR)
				elif body_part.direction is Direction.DOWN: body_part.set_sprite(Snake._TURN_UR)
				else: body_part.set_sprite(Snake._BODY_H)

			elif prev_body_part.direction is Direction.DOWN:
				if body_part.direction is Direction.RIGHT: body_part.set_sprite(Snake._TURN_DR)
				elif body_part.direction is Direction.LEFT: body_part.set_sprite(Snake._TURN_DL)
				else: body_part.set_sprite(Snake._BODY_V)

			else:
				if body_part.direction is Direction.UP: body_part.set_sprite(Snake._TURN_DL)
				elif body_part.direction is Direction.DOWN: body_part.set_sprite(Snake._TURN_UL)
				else: body_part.set_sprite(Snake._BODY_H)

		# correct tail sprite
		tail = self.body[-1]
		prev_body_part = self.body[-2]

		if prev_body_part.direction is Direction.UP: tail.set_sprite(Snake._TAIL_U)
		elif prev_body_part.direction is Direction.LEFT: tail.set_sprite(Snake._TAIL_L)
		elif prev_body_part.direction is Direction.DOWN: tail.set_sprite(Snake._TAIL_D)
		else: tail.set_sprite(Snake._TAIL_R)

	def ate(self, food: Food):
		return self.head.pos == food.pos

	def has_collision(self, pos: Position = None):
		head_pos = self.head.pos
		if pos is not None:
			head_pos = pos

		if head_pos.x < 20 or head_pos.x > (self.w - 40) or head_pos.y < 20 or head_pos.y > (self.h - 40):
			return True

		for i in range(1, len(self.body)):
			if head_pos == self.body[i].pos:
				return True

		return False

	def on_body(self, food: Food):
		for body_part in self.body:
			if body_part.pos == food.pos:
				return True

		return False

	def render(self, display: pygame.surface.Surface):
		for body_part in reversed(self.body):
			body_part.render(display)
