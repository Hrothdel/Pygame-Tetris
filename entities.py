class Piece:
    def __init__(self, position_x, position_y, color):
        self.__blocks = [
            Block(position_x, position_y, color),
            Block(position_x + 1, position_y, color),
            Block(position_x + 2, position_y, color),
            Block(position_x + 1, position_y + 1, color)
        ]

    def getBlocks(self):
        return self.__blocks

class Block:
    def __init__(self, position_x, position_y, color):
        self.__x = position_x
        self.__y = position_y
        self.__color = color

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getColor(self):
        return self.__color
