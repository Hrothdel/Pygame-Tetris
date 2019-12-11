import pygame
import random
import time
from entities import Piece
from entities import Block
from exceptions import Collision

class GameService:
    def __init__(self, grid_columns, grid_rows):
        self.__grid_columns = grid_columns
        self.__grid_rows = grid_rows

        self.__initializeGrid()

        self.__controlled_piece = None

        self.__gravity_interval = 0.7
        self.__gravity_last_time = -1

        self.__pieces_placed = 0
        self.__score = 0
        self.__soft_drop_cells = 0
        self.__hard_drop_cells = 0

        self.__piece_pool = [
            { # T
                'position_x': 3,
                'position_y': -2,
                'rotation_point_x': 1,
                'rotation_point_y': 1,
                'blocks':[
                    {
                        'x': 1,
                        'y': 0,
                    },
                    {
                        'x': 0,
                        'y': 1,
                    },
                    {
                        'x': 1,
                        'y': 1,
                    },
                    {
                        'x': 2,
                        'y': 1,
                    }
                ],
                'color': [255, 0, 0]
            },

            { # Z
                'position_x': 3,
                'position_y': -2,
                'rotation_point_x': 1,
                'rotation_point_y': 1,
                'blocks':[
                    {
                        'x': 0,
                        'y': 0,
                    },
                    {
                        'x': 1,
                        'y': 0,
                    },
                    {
                        'x': 1,
                        'y': 1,
                    },
                    {
                        'x': 2,
                        'y': 1,
                    }
                ],
                'color': [255, 255, 0]
            },

            { # S
                'position_x': 3,
                'position_y': -2,
                'rotation_point_x': 1,
                'rotation_point_y': 1,
                'blocks':[
                    {
                        'x': 1,
                        'y': 0,
                    },
                    {
                        'x': 2,
                        'y': 0,
                    },
                    {
                        'x': 0,
                        'y': 1,
                    },
                    {
                        'x': 1,
                        'y': 1,
                    }
                ],
                'color': [255, 100, 0]
            },

            { # O
                'position_x': 3,
                'position_y': -2,
                'rotation_point_x': 0.5,
                'rotation_point_y': 0.5,
                'blocks':[
                    {
                        'x': 0,
                        'y': 0,
                    },
                    {
                        'x': 1,
                        'y': 0,
                    },
                    {
                        'x': 0,
                        'y': 1,
                    },
                    {
                        'x': 1,
                        'y': 1,
                    }
                ],
                'color': [0, 255, 0]
            },

            { # I
                'position_x': 2,
                'position_y': -2,
                'rotation_point_x': 1.5,
                'rotation_point_y': 0.5,
                'blocks':[
                    {
                        'x': 0,
                        'y': 0,
                    },
                    {
                        'x': 1,
                        'y': 0,
                    },
                    {
                        'x': 2,
                        'y': 0,
                    },
                    {
                        'x': 3,
                        'y': 0,
                    }
                ],
                'color': [0, 100, 255]
            },

            { # L
                'position_x': 3,
                'position_y': -2,
                'rotation_point_x': 1,
                'rotation_point_y': 1,
                'blocks':[
                    {
                        'x': 0,
                        'y': 0,
                    },
                    {
                        'x': 0,
                        'y': 1,
                    },
                    {
                        'x': 1,
                        'y': 1,
                    },
                    {
                        'x': 2,
                        'y': 1,
                    }
                ],
                'color': [0, 0, 255]
            },

            { # J
                'position_x': 3,
                'position_y': -2,
                'rotation_point_x': 1,
                'rotation_point_y': 1,
                'blocks':[
                    {
                        'x': 2,
                        'y': 0,
                    },
                    {
                        'x': 0,
                        'y': 1,
                    },
                    {
                        'x': 1,
                        'y': 1,
                    },
                    {
                        'x': 2,
                        'y': 1,
                    }
                ],
                'color': [200, 150, 0]
            },
        ]

    def __initializeGrid(self):
        self.__grid = []
        extra_rows = 5

        for row_index in range(self.__grid_rows + extra_rows):
            row = []
            for column_index in range(self.__grid_columns + 2):
                if row_index == self.__grid_rows +\
                    extra_rows - 1 or\
                    column_index == 0 or\
                    column_index == self.__grid_columns + 1:
                    row.append(1)
                else:
                    row.append(0)
            self.__grid.append(row)

        self.__grid_offset_x = 1
        self.__grid_offset_y = 4

    def getGridRows(self):
        return self.__grid_rows

    def getGridColumns(self):
        return self.__grid_columns

    def getGrid(self):
        return self.__grid

    def getScore(self):
        return self.__score

    def __removeBlockFromGrid(self, block):
        position_x = block.getX() + self.__grid_offset_x
        position_y = block.getY() + self.__grid_offset_y

        self.__grid[position_y][position_x] = 0

    def __addBlockToGrid(self, block):
        position_x = block.getX() + self.__grid_offset_x
        position_y = block.getY() + self.__grid_offset_y

        self.__grid[position_y][position_x] = block

    def __removePieceFromGrid(self, piece):
        blocks = piece.getBlocks()

        for block in blocks:
            self.__removeBlockFromGrid(block)

    def __checkPieceCollision(self, piece):
        blocks = piece.getBlocks()

        for block in blocks:
            block_x = block.getX() + self.__grid_offset_x
            block_y = block.getY() + self.__grid_offset_y

            if self.__grid[block_y][block_x] != 0:
                raise Collision("Collision")

    def __addPieceToGrid(self, piece):
        blocks = piece.getBlocks()

        self.__checkPieceCollision(piece)

        for block in blocks:
            self.__addBlockToGrid(block)

    def __spawnControlledPiece(self):
        piece = self.__piece_pool[random.randint(0,
            len(self.__piece_pool) - 1)]

        position_x = piece['position_x']
        position_y = piece['position_y']
        rotation_point_x = piece['rotation_point_x']
        rotation_point_y = piece['rotation_point_y']
        color = pygame.Color(piece['color'][0], piece['color'][1],
                             piece['color'][2])
        blocks = []

        for block_info in piece['blocks']:
            blocks.append(Block(block_info['x'], block_info['y']))

        self.__controlled_piece = Piece(position_x, position_y,
            rotation_point_x, rotation_point_y, color, blocks)

        self.__addPieceToGrid(self.__controlled_piece)

    def __clearLines(self, lines):
        lines.sort()

        for line_index in lines:
            for index in range(line_index, 0, -1):
                self.__grid[index] = self.__grid[index-1][:]
                for cell in self.__grid[index]:
                    if type(cell) == Block:
                        cell.setY(cell.getY() + 1)

    def __checkLineClears(self, lines):
        cleared_lines = []

        for line_index in lines:
            line = self.__grid[line_index]

            cleared = True
            for cell in line:
                if cell == 0:
                    cleared = False

            if cleared:
                cleared_lines.append(line_index)

        return cleared_lines

    def __increaseScore(self, clears_number):
        clear_values = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }

        clear_score = clear_values[clears_number]

        soft_drop_score = self.__soft_drop_cells
        hard_drop_score = self.__hard_drop_cells * 2

        soft_drop_score = min(soft_drop_score, 20)
        hard_drop_score = min(hard_drop_score, 40)

        self.__score += clear_score + soft_drop_score +\
            hard_drop_score

        self.__soft_drop_cells = 0
        self.__hard_drop_cells = 0

    def __placePiece(self):
        blocks = self.__controlled_piece.getBlocks()
        lines = []

        for block in blocks:
            block_line = block.getY() + self.__grid_offset_y
            if block_line not in lines:
                lines.append(block_line)

        cleared_lines = self.__checkLineClears(lines)
        self.__clearLines(cleared_lines)
        self.__increaseScore(len(cleared_lines))
        self.__controlled_piece = None
        self.__pieces_placed += 1

    def __movePiece(self, position_x, position_y):
        piece = self.__controlled_piece

        if type(piece) == Piece:
            self.__removePieceFromGrid(piece)
            piece.move(position_x, position_y)

            try:
                self.__addPieceToGrid(piece)
            except Collision:
                piece.move(position_x * (-1), position_y * (-1))
                self.__addPieceToGrid(piece)

                if position_y == 1:
                    self.__placePiece()

    def moveLeft(self):
        self.__movePiece(-1, 0)

    def moveRight(self):
        self.__movePiece(1, 0)

    def moveDown(self):
        self.__movePiece(0, 1)
        if self.__controlled_piece != None:
            self.__soft_drop_cells += 1

    def dropPiece(self):
        piece = self.__controlled_piece

        while piece == self.__controlled_piece:
            self.__movePiece(0, 1)
            self.__hard_drop_cells += 1
        self.__hard_drop_cells -= 1

    def rotateClockwise(self):
        piece = self.__controlled_piece

        self.__removePieceFromGrid(piece)
        piece.rotateClockwise()

        try:
            self.__addPieceToGrid(piece)
        except Collision:
            piece.rotateCounterclockwise()
            self.__addPieceToGrid(piece)

    def rotateCounterclockwise(self):
        piece = self.__controlled_piece

        self.__removePieceFromGrid(piece)
        piece.rotateCounterclockwise()

        try:
            self.__addPieceToGrid(piece)
        except Collision:
            piece.rotateClockwise()
            self.__addPieceToGrid(piece)

    def getControlledPiece(self):
        return self.__controlled_piece

    def __startGravity(self):
        self.__gravity_last_time = time.clock()

    def __handleGravity(self):
        if self.__gravity_last_time != -1:
            if time.clock() - self.__gravity_last_time >=\
                self.__gravity_interval:
                self.__movePiece(0, 1)
                self.__gravity_last_time = time.clock()

    def update(self):
        if self.__controlled_piece == None:
            self.__spawnControlledPiece()
            self.__startGravity()

        self.__handleGravity()
