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
            pygame.K_LEFT: "left",
            pygame.K_a: "left",
            pygame.K_h: "left",
            pygame.K_RIGHT: "right",
            pygame.K_d: "right",
            pygame.K_l: "right",
            pygame.K_DOWN: "soft",
            pygame.K_s: "soft",
            pygame.K_j: "soft",
            pygame.K_UP: "rotate",
            pygame.K_w: "rotate",
            pygame.K_k: "rotate",
            pygame.K_q: "rotatecc",
            pygame.K_SPACE: "hard",
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
            score = self.__service.getScores()
            self.__renderer.render(grid, score)

        self.__quit()

    def __handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit = True
            if event.type == pygame.KEYDOWN:
                if event.key in self.__binds:
                    self.__service.uiAction(
                        self.__binds[event.key])
