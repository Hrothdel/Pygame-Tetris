import pygame
import sys

class UI:
    def __init__(self, service, renderer):
        self.__service = service
        self.__renderer = renderer

        self.__renderer.start()
        self.__renderer.updateGridSize(
            self.__service.getGridRows(),
            self.__service.getGridColumns())
        
        self.__clock = pygame.time.Clock()
        self.__framerate = 60

        self.__exit = False

    def __quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.__exit == False:
            self.__clock.tick(self.__framerate)

            self.__handleInput()

            grid = self.__service.getGrid()
            self.__renderer.render(grid)

        self.__quit()

    def __handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit = True
