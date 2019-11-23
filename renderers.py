import pygame

class GraphicsRenderer:
    def __init__(self, size):
        self.__size = size

        pygame.init()

    def start(self):
        self.__screen = pygame.display.set_mode(self.__size)

    def render(self):
        pygame.display.flip()
