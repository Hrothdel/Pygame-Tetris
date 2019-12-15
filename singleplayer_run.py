import pygame
from renderers import GraphicsRenderer
from services import GameService
from ui import UI

renderer = GraphicsRenderer(1280, 800)
service = GameService(10, 20)
ui = UI(service, renderer)

ui.run()
