import pygame
from entities import Block

class GraphicsRenderer:
    def __init__(self, width, height):
        self.__screen_width = width
        self.__screen_height = height

        self.__grid_width = width / 3
        self.__grid_block_size = 0
        self.__grid_border_thickness = 9

        self.__side_panel_left_width = width / 3
        self.__side_panel_right_width = width / 3

        self.__grid_border_color = pygame.Color(200, 200, 200)
        self.__grid_lines_color = pygame.Color(200, 200, 200)
        self.__background_color = pygame.Color(0, 0, 0)
        self.__grid_lines_thickness = 2

        pygame.init()

    def start(self):
        self.__screen = pygame.display.set_mode((self.__screen_width,
            self.__screen_height))

    def updateGridSize(self, grid_rows, grid_columns):
        self.__grid_rows = grid_rows
        self.__grid_columns = grid_columns

        vertical_space = (self.__screen_height -
            self.__grid_border_thickness * 2) / grid_rows
        horizontal_space = (self.__grid_width -
            self.__grid_border_thickness * 2) / grid_columns

        self.__grid_block_size = min(vertical_space,
            horizontal_space)

        vertical_margin = (self.__screen_height -
            self.__grid_border_thickness * 2 -
            self.__grid_block_size * grid_rows) / 2

        horizontal_margin = (self.__grid_width -
            self.__grid_border_thickness * 2 -
            self.__grid_block_size * grid_columns) / 2

        self.__grid_vertical_margin = vertical_margin
        self.__grid_horizontal_margin = horizontal_margin

        self.__grid_start_x = self.__side_panel_left_width +\
            horizontal_margin + self.__grid_border_thickness
        self.__grid_start_y = vertical_margin +\
            self.__grid_border_thickness

        self.__grid_border_size = (self.__grid_width -
            horizontal_margin * 2 -
            self.__grid_border_thickness * 2,
            self.__screen_height - vertical_margin * 2 -
            self.__grid_border_thickness * 2)

    def __drawRectangle(self, color, rect, thickness):
        top = rect.top
        left = rect.left
        width = rect.width
        height = rect.height

        # Top
        current_rect = pygame.Rect(left - thickness,
            top - thickness, width + thickness * 2, thickness)

        pygame.draw.rect(self.__screen, color, current_rect)
        
        # Left
        current_rect = pygame.Rect(left - thickness,
            top - thickness, thickness, height + thickness * 2)
        pygame.draw.rect(self.__screen, color, current_rect)

        # Bottom
        current_rect = pygame.Rect(left - thickness, top + height, 
            width + thickness * 2, thickness)
        pygame.draw.rect(self.__screen, color, current_rect)

        # Right
        current_rect = pygame.Rect(left + width, top - thickness,
            thickness, height + thickness * 2)
        pygame.draw.rect(self.__screen, color, current_rect)

    def __renderGridBorder(self):
        border_rect = pygame.Rect((self.__grid_start_x,
            self.__grid_start_y), self.__grid_border_size)

        self.__drawRectangle(self.__grid_border_color,
            border_rect, self.__grid_border_thickness)
        #pygame.draw.rect(self.__screen, self.__grid_border_color,
        #    border_rect, self.__grid_border_thickness)

    def __renderGridLines(self):
        # Horizontal lines
        line_start = [self.__side_panel_left_width +
            self.__grid_horizontal_margin +
            self.__grid_border_thickness - 1,
            self.__grid_vertical_margin +
            self.__grid_border_thickness - 1]
        line_end = [self.__side_panel_left_width +
            self.__grid_width -
            self.__grid_horizontal_margin -
            self.__grid_border_thickness - 1,
            self.__grid_vertical_margin +
            self.__grid_border_thickness - 1]

        for _ in range(1, self.__grid_rows):
            line_start[1] += self.__grid_block_size
            line_end[1] += self.__grid_block_size

            pygame.draw.line(self.__screen,
                self.__grid_lines_color,
                line_start, line_end,
                self.__grid_lines_thickness)

        # Vertical lines
        line_start = [self.__side_panel_left_width +
            self.__grid_horizontal_margin +
            self.__grid_border_thickness - 1,
            self.__grid_vertical_margin +
            self.__grid_border_thickness - 1]
        line_end = [self.__side_panel_left_width +
            self.__grid_horizontal_margin +
            self.__grid_border_thickness - 1,
            self.__screen_height - self.__grid_vertical_margin -
            self.__grid_border_thickness - 1]

        for _ in range(1, self.__grid_columns):
            line_start[0] += self.__grid_block_size
            line_end[0] += self.__grid_block_size

            pygame.draw.line(self.__screen,
                self.__grid_lines_color, line_start, line_end,
                self.__grid_lines_thickness)

    def __renderBlock(self, block):
        if block.getY() < 0:
            return

        x = block.getX() * self.__grid_block_size +\
            self.__grid_start_x
        y = block.getY() * self.__grid_block_size +\
            self.__grid_start_y
        color = block.getColor()

        block_rect = pygame.Rect(x, y, self.__grid_block_size,
            self.__grid_block_size)
        
        pygame.draw.rect(self.__screen, color, block_rect)

    def __renderGridBlocks(self, grid):
        for row in grid:
            for element in row:
                if type(element) == Block:
                    self.__renderBlock(element)

    def __renderGrid(self, grid):
        self.__renderGridBorder()
        self.__renderGridLines()
        self.__renderGridBlocks(grid)

    def render(self, grid):
        self.__screen.fill(self.__background_color)

        self.__renderGrid(grid)

        pygame.display.flip()
