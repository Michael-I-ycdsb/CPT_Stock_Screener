"""
The general settings for this project
"""
import pygame

WINDOW_WIDTH = (16 * 64) * 1.2
WINDOW_HEIGHT = (9 * 64) * 1.2

TILE_SIZE = 64

ACTIVE_STATE = {'active_state': None}

FONT_SIZE = 15
TEXT_FONT = 'assets/text/Arial.ttf'

KEYS_PRESSED = {
    pygame.K_F3: False,
    pygame.K_UP: False,
    pygame.K_RIGHT: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
}


# Colors

BACKGROUND_COLOR = (30, 30, 40)
GRAPH_LINE_COLOR = (45, 45, 50)
GRAPH_LINE_NUMBER_COLOR = (100, 100, 100)
GRAPH_CANDLE_BULLISH_COLOR = (20, 200, 20)
GRAPH_CANDLE_BEARISH_COLOR = (200, 20, 20)