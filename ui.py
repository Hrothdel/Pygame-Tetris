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

        self.__binds = {
            pygame.K_LEFT: self.__service.moveLeft,
            pygame.K_a: self.__service.moveLeft,
            pygame.K_h: self.__service.moveLeft,
            pygame.K_RIGHT: self.__service.moveRight,
            pygame.K_d: self.__service.moveRight,
            pygame.K_l: self.__service.moveRight,
            pygame.K_DOWN: self.__service.moveDown,
            pygame.K_s: self.__service.moveDown,
            pygame.K_j: self.__service.moveDown,
            pygame.K_UP: self.__service.rotateClockwise,
            pygame.K_w: self.__service.rotateClockwise,
            pygame.K_k: self.__service.rotateClockwise,
        }

    def __quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.__exit == False:
            self.__clock.tick(self.__framerate)

            self.__handleInput()

            self.__service.update()

            grid = self.__service.getGrid()
            self.__renderer.render(grid)

        self.__quit()

    def __handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit = True
            if event.type == pygame.KEYDOWN:
                if event.key in self.__binds:
                    self.__binds[event.key]()
