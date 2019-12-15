from services import GameClientService

client = GameClientService(10, 20, "localhost", 9999)

while True:
    client.update()
