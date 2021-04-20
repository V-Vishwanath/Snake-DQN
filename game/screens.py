import pygame
from time import sleep

from mlagents.agent import Agent
from game.snake.env import SnakeGame

from game.core import Direction, GameObject
from game.menus import MainMenu, PauseMenu, GameOverMenu


def loading_screen(display: pygame.Surface, env: SnakeGame):
	SnakeGame.play_bgm()

	font = pygame.font.Font('assets/fonts/RockSalt-Regular.ttf', 40)
	font.bold = True

	title = font.render('Game starts in', True, (244, 221, 183))
	shadow = font.render('Game starts in', True, (61, 49, 42))

	title_pos = title.get_rect(center=(320, 150))
	shadow_pos = shadow.get_rect(center=(330, 152))

	seconds_left = 4
	while True:
		seconds_left -= 1

		env.render()

		overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
		pygame.draw.rect(overlay, (0, 0, 0, 200), pygame.Rect(0, 0, 640, 480))
		display.blit(overlay, (0, 0))

		display.blit(shadow, shadow_pos)
		display.blit(title, title_pos)

		text = font.render(str(seconds_left), True, (244, 221, 183))
		text_shadow = font.render(str(seconds_left), True, (61, 49, 42))

		display.blit(text_shadow, text_shadow.get_rect(center=(330, 242)))
		display.blit(text, text.get_rect(center=(320, 240)))

		pygame.display.flip()

		if seconds_left == 0:
			break

		sleep(1)


def play_the_game(display: pygame.Surface):
	env = SnakeGame(display)
	loading_screen(display, env)

	pause_menu = PauseMenu()
	game_over_menu = GameOverMenu()

	clock = pygame.time.Clock()

	game_paused = game_over = False
	bgm_played = False

	game_over_time = 5

	while True:
		clicked = False
		direction = env.snake.head.direction

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			clicked = (
					event.type == pygame.MOUSEBUTTONDOWN and
					event.button == pygame.BUTTON_LEFT
			)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_paused = True

				elif event.key == pygame.K_w and direction is not Direction.DOWN:
					direction = Direction.UP
				elif event.key == pygame.K_a and direction is not Direction.RIGHT:
					direction = Direction.LEFT
				elif event.key == pygame.K_s and direction is not Direction.UP:
					direction = Direction.DOWN
				elif event.key == pygame.K_d and direction is not Direction.LEFT:
					direction = direction.RIGHT

		if not game_paused and not game_over:
			_, game_over, _ = env.step(direction)

		env.render()

		mouse_pos = pygame.mouse.get_pos()

		if game_paused:
			if not bgm_played:
				PauseMenu.play_bgm()
				bgm_played = True

			selected = pause_menu.render(display, mouse_pos, clicked)
			if selected is not None:
				bgm_played = game_paused = False

				if selected == 0:
					SnakeGame.play_bgm()

				elif selected == 1:
					env.reset()
					loading_screen(display, env)

				elif selected == 2:
					break

				elif selected == 3:
					pygame.display.quit()
					quit()

		if game_over:
			if game_over_time <= 0:
				game_over_menu.set_score(env.score)

				if not bgm_played:
					GameOverMenu.play_bgm()
					GameOverMenu.play_game_over()
					bgm_played = True

				selected = game_over_menu.render(display, mouse_pos, clicked)
				if selected is not None:
					bgm_played = game_over = False
					game_over_time = 5

					if selected == 0:
						env.reset()
						loading_screen(display, env)

					elif selected == 1:
						break

					elif selected == 2:
						pygame.display.quit()
						quit()
			else:
				game_over_time -= 1

		pygame.display.flip()
		clock.tick(20)


def watch_agent_play(display: pygame.Surface):
	env = SnakeGame(display)
	agent = Agent(model='assets/snake_agent.pkl')

	loading_screen(display, env)

	pause = PauseMenu()
	clock = pygame.time.Clock()

	game_paused = game_over = False
	bgm_played = False

	while True:
		clicked = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			clicked = (
					event.type == pygame.MOUSEBUTTONDOWN and
					event.button == pygame.BUTTON_LEFT
			)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_paused = True

		if not game_paused:
			state = env.get_state()
			action = agent.predict_action(state)
			_, game_over, _ = env.step(Agent.action_to_dir(env.snake.head.direction, action))

		env.render()

		if game_paused:
			if not bgm_played:
				PauseMenu.play_bgm()
				bgm_played = True

			selected = pause.render(display, pygame.mouse.get_pos(), clicked)
			if selected is not None:
				bgm_played = game_paused = False

				if selected == 0:
					SnakeGame.play_bgm()

				elif selected == 1:
					env.reset()
					loading_screen(display, env)

				elif selected == 2:
					break

				elif selected == 3:
					pygame.display.quit()
					quit()

		pygame.display.flip()

		if game_over:
			sleep(1)
			env.reset()

		clock.tick(25)


def main_screen(display: pygame.Surface):
	icon = GameObject.load_sprite('assets/icon.png', (32, 32))

	pygame.display.set_icon(icon)
	pygame.display.set_caption('Snake DQN Agent')

	menu = MainMenu()
	background = GameObject.load_sprite('assets/background.jpg', display.get_size())

	MainMenu.play_bgm()
	clock = pygame.time.Clock()

	while True:
		clicked = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			clicked = (
				event.type == pygame.MOUSEBUTTONDOWN and
				event.button == pygame.BUTTON_LEFT
			)

		display.blit(background, (0, 0))

		selected = menu.render(display, pygame.mouse.get_pos(), clicked)
		if selected is not None:
			if selected == 0:
				play_the_game(display)

			elif selected == 1:
				watch_agent_play(display)

			else:
				pygame.quit()
				quit()

		pygame.display.flip()
		clock.tick(60)
