import pygame
from enum import Enum
from typing import Tuple, List
from collections import namedtuple

pygame.init()
pygame.font.init()
pygame.mixer.init()


class Direction(Enum):
	UP = 1
	LEFT = 2
	DOWN = 3
	RIGHT = 4


Position = namedtuple('Position', ['x', 'y'])


class GameObject:
	@staticmethod
	def load_sprite(path: str, size: Tuple[int, int]):
		sprite = pygame.image.load(path)
		return pygame.transform.smoothscale(sprite, size)

	def __init__(self, pos: Position, sprite: pygame.surface.Surface):
		self.pos = pos
		self.sprite = sprite

	def set_sprite(self, sprite: pygame.surface.Surface):
		self.sprite = sprite

	def render(self, display: pygame.surface.Surface):
		display.blit(self.sprite, self.pos)


class MenuButton:
	_AUDIO_CHANNEL = pygame.mixer.find_channel(True)
	_AUDIO_CHANNEL.set_volume(0.2)

	_HOVER_SOUND = pygame.mixer.Sound('assets/sfx/hover.mp3')
	_CLICK_SOUND = pygame.mixer.Sound('assets/sfx/select.mp3')

	_FONT = pygame.font.Font('assets/fonts/GloriaHallelujah-Regular.ttf', 25)
	_FONT.bold = True

	def __init__(self, text: str, pos: Tuple[int, int], **kwargs):
		self.text = MenuButton._FONT.render(text, True, kwargs['text_color'])
		self.shadow = MenuButton._FONT.render(text, True, kwargs['shadow_color'])

		self.btn_color = kwargs['btn_color']
		self.btn_outline = kwargs['btn_outline']
		self.btn_hover_outline = kwargs['btn_hover_outline']

		self.offset = 15

		if kwargs['center']:
			text_rect = self.text.get_rect(center=pos)
			self.text_x, self.text_y = text_rect.x, text_rect.y
			self.offset = 0

		else:
			self.text_x, self.text_y = pos

		self.btn_x, self.btn_y = self.text_x - 15, self.text_y - 4

		btn_w, btn_h = self.text.get_width() + 30, self.text.get_height() + 8
		self.btn = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
		self.btn_region = self.btn.get_rect(topleft=(self.btn_x, self.btn_y))

		self.hovered = False

	def render(self, display: pygame.Surface, mouse_pos: Tuple[int, int], clicked=False):
		hover = self.btn_region.collidepoint(mouse_pos)
		selected = False

		if hover != self.hovered:
			self.hovered = not self.hovered
			MenuButton._AUDIO_CHANNEL.set_volume(0.2)
			MenuButton._AUDIO_CHANNEL.play(MenuButton._HOVER_SOUND)

		offset = 0
		outline = self.btn_outline

		if hover:
			if clicked:
				MenuButton._AUDIO_CHANNEL.play(MenuButton._CLICK_SOUND)
				selected = True

			offset = self.offset
			outline = self.btn_hover_outline

		pygame.draw.rect(self.btn, self.btn_color, self.btn.get_rect(), border_radius=50)
		pygame.draw.rect(self.btn, outline, self.btn.get_rect(), 5, border_radius=50)

		display.blit(self.btn, (self.btn_x + offset, self.btn_y))

		if hover: display.blit(self.shadow, (self.text_x + offset + 5, self.text_y + 2))
		display.blit(self.text, (self.text_x + offset, self.text_y))

		return selected


class Menu:
	@staticmethod
	def play_bgm():
		pygame.mixer.music.load('assets/sfx/menu_bgm.mp3')
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)

	def __init__(self, title: str, pos: Tuple[int, int], title_font: pygame.font.Font):
		self.title = title_font.render(title, True, (244, 221, 183))
		self.shadow = title_font.render(title, True, (61, 49, 42))

		self.title_pos = self.title.get_rect(center=pos)
		self.shadow_pos = self.shadow.get_rect(center=(pos[0] + 10, pos[1] + 2))

		self.menu: List[MenuButton] = []

	def render(self, display: pygame.Surface, mouse_pos: Tuple[int, int], clicked: bool):
		display.blit(self.shadow, self.shadow_pos)
		display.blit(self.title, self.title_pos)

		selected = None
		for index, btn in enumerate(self.menu):
			if btn.render(display, mouse_pos, clicked):
				selected = index

		return selected
