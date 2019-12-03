import pygame
from entities import Piece

class GameService:
    def __init__(self, grid_columns, grid_rows):
        self.__grid_columns = grid_columns
        self.__grid_rows = grid_rows

        self.__initializeGrid()

        self.__controlled_piece = None

    def __initializeGrid(self):
        self.__grid = [[0 for _ in range(self.__grid_columns)]
            for _ in range(self.__grid_rows)] 

    def getGridRows(self):
        return self.__grid_rows

    def getGridColumns(self):
        return self.__grid_columns

    def getGrid(self):
        return self.__grid

    def __addPieceToGrid(self, piece):
        blocks = piece.getBlocks()

        for block in blocks:
            self.__grid[block.getX()][block.getY()] = block

    def __spawnControlledPiece(self):
        piece_color = pygame.Color(255, 0, 0)
        self.__controlled_piece = Piece(4, 0, piece_color)

        self.__addPieceToGrid(self.__controlled_piece)

    def getControlledPiece(self):
        return self.__controlled_piece

    def update(self):
        if self.__controlled_piece == None:
            self.__spawnControlledPiece()
