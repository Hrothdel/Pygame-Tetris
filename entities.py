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

    def move(self, position_x, position_y):
        for block in self.__blocks:
            block.setX(block.getX() + position_x)
            block.setY(block.getY() + position_y)

class Block:
    def __init__(self, position_x, position_y, color):
        self.__x = position_x
        self.__y = position_y
        self.__color = color

    def getX(self):
        return self.__x

    def setX(self, x):
        self.__x = x

    def getY(self):
        return self.__y

    def setY(self, y):
        self.__y = y

    def getColor(self):
        return self.__color
