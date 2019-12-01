class GameService:
    def __init__(self, grid_columns, grid_rows):
        self.__grid_columns = grid_columns
        self.__grid_rows = grid_rows

        self.__initializeGrid()
    
    def __initializeGrid(self):
        self.__grid = [[0 for _ in range(self.__grid_columns)]
            for _ in range(self.__grid_rows)] 

    def getGridRows(self):
        return self.__grid_rows

    def getGridColumns(self):
        return self.__grid_columns

    def getGrid(self):
        return self.__grid
