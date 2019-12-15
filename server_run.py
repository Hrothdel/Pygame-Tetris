from networking import GameServer
from networking import GameServerHandler
from services import GameService

server = GameServer(("localhost", 9999), GameServerHandler, 2)

server.serve_forever(0.1)
