import pygame, yfinance
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
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, KEYS_PRESSED, zoomable=True, panable=True)
        self.stock_name = stock_name
        self.side_bar = None
    
    def draw_grid_lines(self) -> None:
        """
        This method draws grid lines onto this class' surface.
        TODO: make the grid lines a set size while zooming to make sure it does not change thickness
        """
        spacing = 55
        origin_multiple = self.origin - Vector2(
            x = self.origin.x - int(self.origin.x / spacing) * spacing,
            y = self.origin.y - int(self.origin.y / spacing) * spacing
        )

        relative_origin = self.origin - origin_multiple

        for line_x_pos in range(int(relative_origin.x), int(self.surface.get_width() + relative_origin.x), spacing):
            line_start_pos = (line_x_pos, 0)
            line_end_pos = (line_x_pos, relative_origin.y + self.surface.get_height())

            pygame.draw.line(self.surface, GRAPH_LINE_COLOR, line_start_pos, line_end_pos)

        for line_y_pos in range(int(relative_origin.y), int(self.surface.get_height() + relative_origin.y), spacing):
            line_start_pos = (0, line_y_pos)
            line_end_pos = (relative_origin.x + self.surface.get_width(), line_y_pos)

            pygame.draw.line(self.surface, GRAPH_LINE_COLOR, line_start_pos, line_end_pos) 

    def draw_side_bar(self, event) -> None:
        """
        This method draws the side bar onto the screen.
        """
        width = 200

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if self.side_bar == None:
                    self.side_bar = SideBar(Vector2(WINDOW_WIDTH - width, 0), width)
                else:
                    self.side_bar = None

    def draw_assets(self) -> None:
        """
        This method draws all assets.
        """
        self.draw_grid_lines()
    
    def draw_non_zoomable_assets(self):
        """
        This method draws all assets that are always on screen and not zoomable.
        """
        if not self.side_bar == None:
            self.side_bar.draw()

            self.display_surface.blit(self.side_bar.surface, (WINDOW_WIDTH - self.side_bar.rect.width, 0))
    
    def event_loop(self, event) -> None:
        """
        """
        self.draw_side_bar(event)
        

    def run(self) -> None:
        print(self.side_bar)
        return super().run()

class SideBar():
    def __init__(
            self,
            position: Vector2,
            width: float
    ) -> None:
        """
        """
        self.rect = pygame.Rect(position, (width, WINDOW_HEIGHT))
        self.surface = pygame.Surface(self.rect.size)

    def draw(self) -> None:
        self.surface.fill((205, 205, 205))