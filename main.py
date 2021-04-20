import pygame

from game.screens import main_screen

pygame.init()
pygame.font.init()
pygame.mixer.init()

display = pygame.display.set_mode((640, 480))
main_screen(display)
