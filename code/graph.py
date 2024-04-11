import pygame, yfinance, sys
from pygame.math import Vector2
from settings import *
from support.app_state import AppState



class Graph(AppState):
    def __init__(
            self,
            stock_name: str
    ) -> None:
        """
        Appstate
        --------
        This class displays a stock with its info in a graph.

        Parameters
        ----------
        stock_name : str
        """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, KEYS_PRESSED)
        self.stock_name = stock_name
    
    def draw_grid_lines(self) -> None:
        """
        This method draws grid lines onto this class' surface
        TODO: make the grid lines a set size while zooming to make sure it does not change thickness
        """
        spacing = 15

        for line_x_pos in range(int(self.origin.x), int(self.surface.get_width() + self.origin.x), spacing):
            line_start_pos = (line_x_pos, self.origin.y)
            line_end_pos = (line_x_pos, self.origin.y + self.surface.get_height())

            pygame.draw.line(self.surface, (0, 0, 0), line_start_pos, line_end_pos)

        for line_y_pos in range(int(self.origin.y), int(self.surface.get_height() + self.origin.y), spacing):
            line_start_pos = (self.origin.x, line_y_pos)
            line_end_pos = (self.origin.x + self.surface.get_width(), line_y_pos)

            pygame.draw.line(self.surface, (0, 0, 0), line_start_pos, line_end_pos)

    def draw_assets(self) -> None:
        """
        This method draws all assets
        """
        self.draw_grid_lines()

    def run(self) -> None:
        return super().run()

