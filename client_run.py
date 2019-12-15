from networking import GameClientService
from renderers import GraphicsRenderer
from ui import UI

renderer = GraphicsRenderer(1280, 800)
client = GameClientService(10, 20, "localhost", 9999)
ui = UI(client, renderer)

ui.run()
