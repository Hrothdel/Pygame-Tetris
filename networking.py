import socketserver
import socket
import time
from services import GameService

class GameServerHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).decode().\
            strip().split()

        if len(self.data) > 0:
            command = self.data[0]
            parameters = self.data[1:]

            if command in self.server.commands:
                try:
                    self.request.sendall(self.server.\
                        commands[command](parameters).encode())
                except ValueError:
                    self.request.sendall("Invalid request".\
                        encode())

class GameServer(socketserver.TCPServer):
    def __init__(self, address, handler_class, player_number):
        self.commands = {
            "connect": self.connectPlayer,
            "update": self.updatePlayer
        }
        self.player_number = player_number
        self.update_queues = []

        socketserver.TCPServer.__init__(self, address,
            handler_class)

    def getConnectedPlayersCount(self):
        return len(self.update_queues)

    def connectPlayer(self, parameters):
        if len(parameters) != 0:
            raise ValueError("Invalid number of parameters")

        player_number = self.getConnectedPlayersCount() + 1

        self.update_queues.append([])

        if player_number == self.player_number:
            self.startGame()

        return str(player_number - 1)
    
    def updatePlayer(self, parameters):
        if len(parameters) != 1:
            raise ValueError("Invalid number of parameters")

        player_index = int(parameters[0])
        update_string = ""

        for update in self.update_queues[player_index]:
            update_string += ";" + update

        self.update_queues[player_index] = []

        if update_string == "":
            update_string = "none"
        return update_string

    def startGame(self):
        self.__addToQueue("start")

    def __addToQueue(self, update_text, exclude = []):
        for index in range(self.getConnectedPlayersCount()):
            if index not in exclude:
                self.update_queues[index].append(update_text)

class GameClientService(GameService):
    def __init__(self, grid_columns, grid_rows, host_ip,
        server_port):
        self.__host_ip = host_ip
        self.__server_port = server_port
        GameService.__init__(self, grid_columns, grid_rows)

        self.__connected = False
        self.__client_index = -1
        self.__started = False
        self.__server_update_interval = 1
        self.__last_server_update_time = 0

        self.__update_commands = {
            "start": self.start,
        }

    def update(self):
        if self.__connected == False:
            self.connect()
        else:
            if self.__started:
                GameService.update(self)
            self.handleConnection()

    def handleConnection(self):
        if time.clock() - self.__last_server_update_time >=\
            self.__server_update_interval:
            self.requestServerUpdate()

    def requestServerUpdate(self):
        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))
        self.__client.sendall(("update " +
            str(self.__client_index)).encode())
        update_response = self.__client.recv(1024).decode()

        self.handleUpdate(update_response)

        self.__last_server_update_time = time.clock()

    def handleUpdate(self, update_response):
        parts = update_response.split(";")

        for update_part in parts:
            if update_part in self.__update_commands:
                self.__update_commands[update_part]()
            elif update_part != "none":
                print("Invalid update command: " +
                    update_part)

    def connect(self):
        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))

        self.__client.sendall("connect".encode())
        recieved = self.__client.recv(1024).decode()
        self.__client_index = int(recieved)
        self.__connected = True

    def start(self):
        self.__started = True
