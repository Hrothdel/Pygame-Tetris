from renderers import GraphicsRenderer
from services import GameService
from ui import UI

renderer = GraphicsRenderer((1280, 800))
service = GameService(5, 10)
ui = UI(service, renderer)

ui.run()
