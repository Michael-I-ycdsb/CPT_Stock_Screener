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

        self.text_font = pygame.font.Font(TEXT_FONT, FONT_SIZE)
    
    def draw_grid_lines(self) -> None:
        """
        This method draws grid lines onto this class' surface.
        TODO: make the grid lines a set size while zooming to make sure it does not change thickness
        """
        spacing = Vector2(100, 55)
        origin_multiple = self.origin - Vector2(
            x = self.origin.x - int(self.origin.x / spacing.x) * spacing.x,
            y = self.origin.y - int(self.origin.y / spacing.y) * spacing.y
        )

        relative_origin = self.origin - origin_multiple

        for line_x_pos in range(int(relative_origin.x), int(self.surface.get_width() + relative_origin.x), int(spacing.x)):
            line_start_pos = (line_x_pos, 0)
            line_end_pos = (line_x_pos, relative_origin.y + self.surface.get_height())

            pygame.draw.line(self.surface, GRAPH_LINE_COLOR, line_start_pos, line_end_pos)

            number = -int(self.origin.x / spacing.x) + ((line_x_pos // spacing.x) - (relative_origin.x // spacing.x))
            self.draw_grid_number(line_y=line_x_pos, number=number)

        for line_y_pos in range(int(relative_origin.y), int(self.surface.get_height() + relative_origin.y), int(spacing.y)):
            line_start_pos = (0, line_y_pos)
            line_end_pos = (relative_origin.x + self.surface.get_width(), line_y_pos)

            pygame.draw.line(self.surface, GRAPH_LINE_COLOR, line_start_pos, line_end_pos)

            number = -int(self.origin.y / spacing.y) + ((line_y_pos // spacing.y) - (relative_origin.y // spacing.y))
            self.draw_grid_number(line_x=line_y_pos, number=number)

    def draw_grid_number(
            self,
            line_x: float = 0,
            line_y: float = 0,
            number: float = 0
    ) -> None:
        """
        Draws a grid number at the given position

        Parameters
        ----------
        line_x : float = 0
            The x position of the line to draw the number on. Only define if the number is on the x lines.
        line_y : float = 0
            The y position of the line to draw the number on. Only define if the number is on the y lines.
        number : float = 0
            The number that will be drawn.
        """
        number_surface = self.text_font.render(str(number), True, GRAPH_LINE_NUMBER_COLOR, BACKGROUND_COLOR)
        number_rect = number_surface.get_rect()
        if line_x != 0: number_rect.center = Vector2(WINDOW_WIDTH - number_rect.w, line_x)
        if line_y != 0: number_rect.center = Vector2(line_y, WINDOW_HEIGHT - number_rect.h)

        self.surface.blit(number_surface, number_rect)

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