class Piece:
    def __init__(self, position_x, position_y, color):
        self.__blocks = [
            Block(position_x, position_y, color),
            Block(position_x + 1, position_y, color),
            Block(position_x + 2, position_y, color),
            Block(position_x + 1, position_y + 1, color)
        ]

        self.__rotation_point_x = position_x + 1
        self.__rotation_point_y = position_y

    def rotateClockwise(self):
        for block in self.__blocks:
            block_x = block.getX()
            block_y = block.getY()

            block.setX((block_y - self.__rotation_point_y) *
                (-1) + self.__rotation_point_x)
            block.setY((block_x - self.__rotation_point_x) +
                self.__rotation_point_y)

    def rotateCounterclockwise(self):
        for block in self.__blocks:
            block_x = block.getX()
            block_y = block.getY()

            block.setX(block_y)
            block.setY(block_x * (-1))

    def getBlocks(self):
        return self.__blocks

    def move(self, position_x, position_y):
        for block in self.__blocks:
            block.setX(block.getX() + position_x)
            block.setY(block.getY() + position_y)

        self.__rotation_point_x += position_x
        self.__rotation_point_y += position_y

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
