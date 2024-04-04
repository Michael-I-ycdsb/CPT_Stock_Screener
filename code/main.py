import pygame
from settings import *
from graph import graph

class Main():
    def __init__(self) -> None:
        """
        Manages the screen and updating the program
        """

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED).convert_alpha()
        self.clock = pygame.time.Clock()
        self.app_state = AppState()

    def run(self) -> None:
        """
        Runs the while loop of the code 60 times every second and updates display
        """

        while True:
            
            self.app_state.state_manager()
            
            pygame.display.update()
            self.clock.tick(60)
            #print(self.clock.get_fps())

class AppState():
    def __init__(self) -> None:
        """
        Manages the current state that needs to run
        """

        self.graph = graph()

    def state_manager(self) -> None:
        """
        Runs which ever state is currently active
        """

        if ACTIVE_STATE['active_state'] == 'sim':
            self.graph.run()

if __name__ == '__main__':
    main = Main()
    main.run()
    
    #profile.runctx('main.run()', globals(), locals())