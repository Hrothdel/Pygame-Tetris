from renderers import GraphicsRenderer
from services import GameService
from ui import UI

renderer = GraphicsRenderer((1240, 960))
service = GameService()
ui = UI(service, renderer)

ui.run()
