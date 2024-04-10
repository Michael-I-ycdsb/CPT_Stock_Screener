import pygame, sys
from pygame.math import Vector2

class AppState():
    def __init__(
            self,
            window_width: int,
            window_height: int,
            background_color: tuple[int, int, int],
            keys_pressed: dict
    ) -> None:
        """
        Parent Class
        ------------
        This is a parent class that creates a runable state in pygame.

        Parameters
        ----------
        window_width : int
        window_height : int
        background_color : tuple[int, int, int]
        keys_pressed : dict
        """
        self.__background_color = background_color
        self.__keys_pressed = keys_pressed

        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((window_width * 3, window_height * 3)).convert_alpha()
        self.origin = Vector2(0, 0)
        self.zoom = 1
    
    def manage_window(self, event) -> None:
        """
        This method manages when to quit application, when to toggle fullscreen,
        and when to zoom.

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
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
        """
        This method updates which of the keys in the dict __keys_pressed has
        been pressed or unpressed.

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
        if event.type == pygame.KEYDOWN:
            for key in self.__keys_pressed:
                if event.key == key:
                    if self.__keys_pressed[key] == True:
                        self.__keys_pressed[key] = False
                    else:
                        self.__keys_pressed[key] = True

    def event_loop(self) -> None:
        """
        This method manages all events and calls all methods with the event parameter
        """
        for event in pygame.event.get():
            
            self.manage_window(event)
            self.update_keys_pressed(event)
    
    def draw_assets(self) -> None:
        """
        This method is empty and is meant to be overwritten
        """

    def draw(self) -> None:
        """
        This method draws the background first, then it draws the origin point,
        then it draws the zoomed screen depending on how zoomed the screen is.
        """
        self.surface.fill((self.__background_color))

        self.draw_assets()

        pygame.draw.circle(self.surface, (250, 0, 0), self.origin, 10)

        zoomed_screen = pygame.transform.smoothscale_by(self.surface, self.zoom)
        self.display_surface.blit(zoomed_screen, Vector2(0, 0))

    def run(self) -> None:
        """
        This method runs both the event_loop and the draw methods and this
        is the only method needed to be called for this class to function.
        """

        self.event_loop()
            
        self.draw()