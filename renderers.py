import pygame

class GraphicsRenderer:
    def __init__(self, size):
        self.__size = size

        self.__grid_width = size[0] / 3
        self.__grid_block_size = 0
        self.__grid_border_thickness = 5

        self.__side_panel_left_width = size[0] / 3
        self.__side_panel_right_width = size[0] / 3

        self.__grid_border_color = pygame.Color(200, 200, 200)

        pygame.init()

    def start(self):
        self.__screen = pygame.display.set_mode(self.__size)

    def updateGridSize(self, grid_rows, grid_columns):
        vertical_space = (self.__size[1] -
            self.__grid_border_thickness * 2) / grid_rows
        horizontal_space = (self.__grid_width -
            self.__grid_border_thickness * 2) / grid_columns

        self.__grid_block_size = min(vertical_space,
            horizontal_space)

        vertical_margin = (self.__size[1] -
            self.__grid_border_thickness * 2 -
            self.__grid_block_size * grid_rows) / 2

        horizontal_margin = (self.__grid_width -
            self.__grid_border_thickness * 2 -
            self.__grid_block_size * grid_columns) / 2

        self.__grid_border_start = (self.__side_panel_left_width +
            horizontal_margin + self.__grid_border_thickness // 2,
            vertical_margin + self.__grid_border_thickness // 2)

        self.__grid_border_size = (self.__grid_width +
            self.__grid_border_thickness // 2,
            self.__size[1] - vertical_margin -
            self.__grid_border_thickness // 2)

    def render(self, grid):
        self.__renderGrid(grid)

        pygame.display.flip()

    def __renderGridBorder(self):
        border_rect = pygame.Rect(self.__grid_border_start,
            self.__grid_border_size)

        pygame.draw.rect(self.__screen, self.__grid_border_color,
            border_rect, self.__grid_border_thickness)

    def __renderGrid(self, grid):
        self.__renderGridBorder()
