import pygame
from entities import Piece
from entities import Block
from exceptions import Collision

class GameService:
    def __init__(self, grid_columns, grid_rows):
        self.__grid_columns = grid_columns
        self.__grid_rows = grid_rows

        self.__initializeGrid()

        self.__controlled_piece = None

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
        piece_color = pygame.Color(255, 0, 0)
        self.__controlled_piece = Piece(3, -2, piece_color)

        self.__addPieceToGrid(self.__controlled_piece)

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
                    self.__spawnControlledPiece()

    def moveLeft(self):
        self.__movePiece(-1, 0)

    def moveRight(self):
        self.__movePiece(1, 0)

    def moveDown(self):
        self.__movePiece(0, 1)

    def dropPiece(self):
        piece = self.__controlled_piece

        while piece == self.__controlled_piece:
            self.__movePiece(0, 1)

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

    def update(self):
        if self.__controlled_piece == None:
            self.__spawnControlledPiece()
