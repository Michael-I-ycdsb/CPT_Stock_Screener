"""
The general settings for this project
"""
import pygame

WINDOW_WIDTH = (16 * 64) * 1.2
WINDOW_HEIGHT = (9 * 64) * 1.2

TILE_SIZE = 64

ACTIVE_STATE = {'active_state': None}

TEXT_FONT = 'assets/text/PoetsenOne-Regular.ttf'

KEYS_PRESSED = {
    pygame.K_F3: False,
    pygame.K_UP: False,
    pygame.K_RIGHT: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
}


# Colors

BACKGROUND_COLOR = (255, 255, 255)