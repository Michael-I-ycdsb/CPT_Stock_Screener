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
    
    def run(self) -> None:
        return super().run()

