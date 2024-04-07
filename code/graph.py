import pygame, yfinance, sys
from settings import *
from pygame.math import Vector2

class AppState():
    def __init__(
            self,
            window_width: int,
            window_height: int,
            background_color: tuple(int, int, int)
    ) -> None:
        """
        Parent Class
        ------------
        This is a parent class that creates a runable state in pygame.

        Parameters
        ----------
        None
        """
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((WINDOW_WIDTH * 3, WINDOW_HEIGHT * 3)).convert_alpha()
        self.origin = Vector2(0, 0)
        self.zoom = 1
    
    def manage_window(self, event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.WINDOWMAXIMIZED:
            pygame.display.toggle_fullscreen()
        if event.type == pygame.WINDOWMINIMIZED:
            pygame.display.toggle_fullscreen()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_MINUS and self.zoom > 0.5:
                    self.zoom -= 0.1
                if event.key == pygame.K_EQUALS and self.zoom < 2:
                    self.zoom += 0.1

    def update_keys_pressed(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            for key in KEYS_PRESSED:
                if event.key == key:
                    if KEYS_PRESSED[key] == True:
                        KEYS_PRESSED[key] = False
                    else:
                        KEYS_PRESSED[key] = True

    def event_loop(self) -> None:
        for event in pygame.event.get():
            
            self.manage_window(event)
            self.update_keys_pressed(event)

    def draw(self) -> None:
        self.surface.fill((BACKGROUND_COLOR))

        pygame.draw.circle(self.surface, (250, 0, 0), self.origin, 10)

        zoomed_screen = pygame.transform.smoothscale_by(self.surface, self.zoom)
        self.display_surface.blit(zoomed_screen, Vector2(0, 0))

    def run(self) -> None:

        self.event_loop()
            
        self.draw()


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
        super().__init__()
        self.stock_name = stock_name
