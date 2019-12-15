from services import GameServer
from services import GameServerHandler
from services import GameService

server = GameServer(("localhost", 9999), GameServerHandler, 2)

server.serve_forever(0.1)
