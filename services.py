import pygame
from entities import Piece

class GameService:
    def __init__(self, grid_columns, grid_rows):
        self.__grid_columns = grid_columns
        self.__grid_rows = grid_rows

        self.__initializeGrid()

        self.__controlled_piece = None

    def __initializeGrid(self):
        self.__grid = []

        for _ in range(self.__grid_rows):
            row = []
            for _ in range(self.__grid_columns):
                row.append(0)
            self.__grid.append(row)

    def getGridRows(self):
        return self.__grid_rows

    def getGridColumns(self):
        return self.__grid_columns

    def getGrid(self):
        return self.__grid

    def __removeBlockFromGrid(self, block):
        position_x = block.getX()
        position_y = block.getY()

        self.__grid[position_y][position_x] = 0

    def __addBlockToGrid(self, block):
        position_x = block.getX()
        position_y = block.getY()

        self.__grid[position_y][position_x] = block

    def __removePieceFromGrid(self, piece):
        blocks = piece.getBlocks()

        for block in blocks:
            self.__removeBlockFromGrid(block)

    def __addPieceToGrid(self, piece):
        blocks = piece.getBlocks()

        for block in blocks:
            self.__addBlockToGrid(block)

    def __spawnControlledPiece(self):
        piece_color = pygame.Color(255, 0, 0)
        self.__controlled_piece = Piece(4, 0, piece_color)

        self.__addPieceToGrid(self.__controlled_piece)

    def __movePiece(self, position_x, position_y):
        piece = self.__controlled_piece

        if type(piece) == Piece:
            self.__removePieceFromGrid(piece)
            piece.move(position_x, position_y)
            self.__addPieceToGrid(piece)

    def moveLeft(self):
        self.__movePiece(-1, 0)

    def moveRight(self):
        self.__movePiece(1, 0)
    
    def moveDown(self):
        self.__movePiece(0, 1)

    def getControlledPiece(self):
        return self.__controlled_piece

    def update(self):
        if self.__controlled_piece == None:
            self.__spawnControlledPiece()
