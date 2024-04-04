import pygame, yfinance, sys
from settings import *

class graph():
    def __init__(
            self,
            stock: str
    ) -> None:
        """
        Appstate

        This class displays a stock with its info in a graph

        Parameters
        ----------
        stock : str

        """