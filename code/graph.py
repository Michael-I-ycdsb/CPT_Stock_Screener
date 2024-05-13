import pygame, yfinance
import datetime
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

        self.graph_count_interval = Vector2(10, 0.1)
        self.graph_spacing = Vector2(100, 60)
        self.current_datetime = datetime.datetime.now()

        self.origin = Vector2(0, self.graph_spacing.y * 1800)
        self.period = "1d"
        self.interval = "5m"
        self.stock_data = yfinance.download(tickers=self.stock_name, period=self.period, interval=self.interval)
        self.datetime_stock_data = yfinance.download(tickers=self.stock_name, period=self.period, interval=self.interval)
        self.datetime_stock_data.reset_index(inplace=True)
    
    def draw_grid_lines(self) -> None:
        """
        This method draws grid lines onto this class' surface.
        TODO: make the grid lines a set size while zooming to make sure it does not change thickness
        """
        origin_multiple = self.origin - Vector2(
            x = self.origin.x - int(self.origin.x / self.graph_spacing.x) * self.graph_spacing.x,
            y = self.origin.y - int(self.origin.y / self.graph_spacing.y) * self.graph_spacing.y
        )

        relative_origin = self.origin - origin_multiple

        for line_x_pos in range(int(relative_origin.x), int(self.surface.get_width() + relative_origin.x), int(self.graph_spacing.x)):
            line_start_pos = (line_x_pos, 0)
            line_end_pos = (line_x_pos, relative_origin.y + self.surface.get_height())

            pygame.draw.line(self.surface, GRAPH_LINE_COLOR, line_start_pos, line_end_pos)

            # scale for graph
            scale_num_from_origin = int(-int(self.origin.x / self.graph_spacing.x) + ((line_x_pos // self.graph_spacing.x) - (relative_origin.x // self.graph_spacing.x)))
            hour = str(self.current_datetime.hour + int((scale_num_from_origin * self.graph_count_interval.x) / 60))
            minute = str(int((scale_num_from_origin * self.graph_count_interval.x) % 60)) + "0"
            scale_num = f"{hour}:{minute[:2]}"

            self.draw_grid_number(line_y=line_x_pos, number=scale_num)

        for line_y_pos in range(int(relative_origin.y), int(self.surface.get_height() + relative_origin.y), int(self.graph_spacing.y)):
            line_start_pos = (0, line_y_pos)
            line_end_pos = (relative_origin.x + self.surface.get_width(), line_y_pos)

            pygame.draw.line(self.surface, GRAPH_LINE_COLOR, line_start_pos, line_end_pos)

            scale_num_from_origin = -int(self.origin.y / self.graph_spacing.y) + ((line_y_pos // self.graph_spacing.y) - (relative_origin.y // self.graph_spacing.y))
            self.draw_grid_number(line_x=line_y_pos, number=str(round(-scale_num_from_origin * self.graph_count_interval.y, 2)))

    def draw_grid_number(
            self,
            line_x: float = 0,
            line_y: float = 0,
            number: str = "None"
    ) -> None:
        """
        Draws a grid number at the given position

        Parameters
        ----------
        line_x : float = 0
            The x position of the line to draw the number on. Only define if the number is on the x lines.
        line_y : float = 0
            The y position of the line to draw the number on. Only define if the number is on the y lines.
        number : str = "None"
            The number that will be drawn.
        """
        number_surface = self.text_font.render(number, True, GRAPH_LINE_NUMBER_COLOR, BACKGROUND_COLOR)
        number_rect = number_surface.get_rect()
        if line_x != 0: number_rect.center = Vector2(WINDOW_WIDTH - number_rect.w, line_x)
        if line_y != 0: number_rect.center = Vector2(line_y, WINDOW_HEIGHT - number_rect.h)

        self.surface.blit(number_surface, number_rect)

    def draw_candle(
            self,
            candle_open: float,
            candle_high: float,
            candle_low: float,
            candle_close: float,
            time: dict["hour": int, "minute": int]
        ) -> None:
        #stock = yfinance.Ticker(self.stock_name)
        
        x_pos = (
            (time["hour"] - self.current_datetime.hour) * (int(60 / self.graph_count_interval.x) * self.graph_spacing.x) # hour location calculation
            + ((time["minute"]) * (self.graph_spacing.x / self.graph_count_interval.x)) # minute location calculation
        )
        graph_spacing_multiple = Vector2(self.graph_spacing.x / self.graph_count_interval.x, self.graph_spacing.y / self.graph_count_interval.y)

        candle_rect = pygame.Rect(0, 0,
                int(graph_spacing_multiple.x * (int(self.interval[:-1]))) - 1,
                int(graph_spacing_multiple.y * abs(candle_open - candle_close))
            )

        if candle_open < candle_close:
            candle_rect.midbottom = self.origin + (x_pos, -candle_open * graph_spacing_multiple.y)
            pygame.draw.rect(
                self.surface,
                GRAPH_CANDLE_BULLISH_COLOR,
                candle_rect
            )
            pygame.draw.line(
                self.surface,
                GRAPH_CANDLE_BULLISH_COLOR,
                (candle_rect.centerx, abs(candle_low - candle_close) * graph_spacing_multiple.y + candle_rect.top),
                (candle_rect.centerx, -abs(candle_high - candle_open) * graph_spacing_multiple.y + candle_rect.bottom)
            )
        else:
            candle_rect.midtop = self.origin + (x_pos, -candle_open * graph_spacing_multiple.y)
            pygame.draw.rect(
                self.surface,
                GRAPH_CANDLE_BEARISH_COLOR,
                candle_rect
            )
            pygame.draw.line(
                self.surface,
                GRAPH_CANDLE_BEARISH_COLOR,
                (candle_rect.centerx, abs(candle_low - candle_close) * graph_spacing_multiple.y + candle_rect.top),
                (candle_rect.centerx, -abs(candle_high - candle_open) * graph_spacing_multiple.y + candle_rect.bottom)
            )

    def create_candles(self) -> None:
        """
        """
        candle_datetime_list = []
        
        for datetime in self.datetime_stock_data["Datetime"]:
            candle_data = self.stock_data.at_time(datetime)
            #print(datetime.hour, candle_data.Open.iloc[0])
            self.draw_candle(candle_data.Open.iloc[0], candle_data.High.iloc[0], candle_data.Low.iloc[0], candle_data.Close.iloc[0], {"hour": datetime.hour, "minute": datetime.minute})

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
        self.create_candles()
        #self.draw_candle(5, 25, 0, 20, {"hour": 9, "minute": 25})
    
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
        print(self.pan_active)
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