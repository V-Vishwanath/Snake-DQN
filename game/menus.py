import pygame
from typing import Tuple

from game.core import Menu, MenuButton

pygame.init()
pygame.font.init()
pygame.mixer.init()


class MainMenu(Menu):
	_FONT = pygame.font.Font('assets/fonts/RockSalt-Regular.ttf', 70)
	_FONT.bold = True

	class MenuItem(MenuButton):
		def __init__(self, text: str, pos: Tuple[int, int]):
			super().__init__(
				text, pos, center=False, text_color=(244, 221, 183), shadow_color=(61, 49, 42),
				btn_color=(125, 95, 80), btn_outline=(100, 67, 60), btn_hover_outline=(71, 33, 24)
			)

	def __init__(self):
		super(MainMenu, self).__init__('Snake!', (320, 70), MainMenu._FONT)
		self.menu = [
			MainMenu.MenuItem('Play the Game', (100, 200)),
			MainMenu.MenuItem('Watch Agent Play', (100, 260)),
			MainMenu.MenuItem('Quit', (100, 320))
		]


class PauseMenu(Menu):
	_FONT = pygame.font.Font('assets/fonts/RockSalt-Regular.ttf', 40)
	_FONT.bold = True

	OVERLAY = pygame.Surface((640, 480), pygame.SRCALPHA)
	pygame.draw.rect(OVERLAY, (0, 0, 0, 200), pygame.Rect(0, 0, 640, 480))

	class MenuItem(MenuButton):
		def __init__(self, text: str, pos: Tuple[int, int]):
			super().__init__(
				text, pos, center=True, text_color=(255, 255, 255), shadow_color=(70, 70, 70),
				btn_color=(201, 50, 50), btn_outline=(143, 1, 1), btn_hover_outline=(107, 0, 0)
			)

	def __init__(self):
		super(PauseMenu, self).__init__('Game Paused!', (320, 90), PauseMenu._FONT)
		self.menu = [
			PauseMenu.MenuItem('Resume', (320, 180)),
			PauseMenu.MenuItem('Restart', (320, 245)),
			PauseMenu.MenuItem('Main Menu', (320, 309)),
			PauseMenu.MenuItem('Quit', (320, 374))
		]

	def render(self, display: pygame.Surface, mouse_pos: Tuple[int, int], clicked: bool):
		display.blit(PauseMenu.OVERLAY, (0, 0))
		return super(PauseMenu, self).render(display, mouse_pos, clicked)


class GameOverMenu(Menu):
	_FONT = pygame.font.Font('assets/fonts/RockSalt-Regular.ttf', 40)
	_FONT.bold = True

	_SCORE_FONT = pygame.font.Font('assets/fonts/GloriaHallelujah-Regular.ttf', 35)

	OVERLAY = pygame.Surface((640, 480), pygame.SRCALPHA)
	pygame.draw.rect(OVERLAY, (0, 0, 0, 200), pygame.Rect(0, 0, 640, 480))

	_GAME_OVER_SOUND = pygame.mixer.Sound('assets/sfx/game_over.mp3')

	@staticmethod
	def play_game_over():
		GameOverMenu._GAME_OVER_SOUND.play()

	class MenuItem(MenuButton):
		def __init__(self, text: str, pos: Tuple[int, int]):
			super().__init__(
				text, pos, center=True, text_color=(255, 255, 255), shadow_color=(70, 70, 70),
				btn_color=(201, 50, 50), btn_outline=(143, 1, 1), btn_hover_outline=(107, 0, 0)
			)

	def __init__(self):
		super(GameOverMenu, self).__init__('Game Over!', (320, 90), GameOverMenu._FONT)
		self.menu = [
			PauseMenu.MenuItem('Restart', (320, 245)),
			PauseMenu.MenuItem('Main Menu', (320, 309)),
			PauseMenu.MenuItem('Quit', (320, 374))
		]

		self.score = None
		self.score_pos = None

	def set_score(self, score: int):
		self.score = GameOverMenu._SCORE_FONT.render(f'Score: {score}', True, (255, 162, 156))
		self.score_pos = self.score.get_rect(center=(320, 160))

	def render(self, display: pygame.Surface, mouse_pos: Tuple[int, int], clicked: bool):
		display.blit(PauseMenu.OVERLAY, (0, 0))
		display.blit(self.score, self.score_pos)
		return super(GameOverMenu, self).render(display, mouse_pos, clicked)
