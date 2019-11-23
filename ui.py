import pygame

class UI:
    def __init__(self, service, renderer):
        self.__service = service
        self.__renderer = renderer

        self.__renderer.start()
        self.__exit = False

    def run(self):

        while self.__exit == False:
            self.__handleInput()
            self.__renderer.render()

    def __handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit = True
