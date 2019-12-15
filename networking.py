import socketserver
import socket
import time
import random
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
                    response = str(self.server.\
                        commands[command](parameters))
                    self.request.sendall(response.encode())
                except ValueError:
                    self.request.sendall("Invalid request".\
                        encode())

class GameServer(socketserver.TCPServer):
    def __init__(self, address, handler_class, player_number):
        self.commands = {
            "connect": self.connectPlayer,
            "update": self.updatePlayer,
            "players_number": self.getConnectedPlayersCount,
            "announce_action": self.announceAction,
            "spawn_piece": self.spawnPiece,
            "end_turn": self.endPlayerTurn,
        }
        self.player_number = player_number
        self.update_queues = []
        self.__piece_pool_size = 7

        socketserver.TCPServer.__init__(self, address,
            handler_class)

    def __addToQueue(self, update_text, exclude = []):
        for index in range(self.getConnectedPlayersCount()):
            if index not in exclude:
                self.update_queues[index].append(update_text)

    def getConnectedPlayersCount(self, *dump):
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

    def endPlayerTurn(self, parameters):
        if len(parameters) != 1:
            raise ValueError("Invalid number of parameters")

        player_index = int(parameters[0])

        next_player = (player_index + 1) %\
            self.getConnectedPlayersCount()

        self.update_queues[next_player].append("activate")

        return "Success"

    def startGame(self):
        self.__addToQueue("start")
        self.update_queues[0].append("activate")

    def spawnPiece(self, parameters):
        if len(parameters) != 1:
            raise ValueError("Invalid number of parameters")

        announcer_index = int(parameters[0])
        piece_index = random.randint(0,
            self.__piece_pool_size - 1)
        self.announceAction(["spawn", str(piece_index),
            announcer_index])
        
        return str(piece_index)

    def announceAction(self, parameters):
        action = parameters[0]
        action_parameters = parameters[1:-1]
        announcer_index = int(parameters[-1])

        update_string = action
        for parameter in action_parameters:
            update_string += " " + parameter
        update_string += " " + str(announcer_index)

        for index in range(self.getConnectedPlayersCount()):
            if index != announcer_index:
                self.update_queues[index].append(update_string)
        return "Success"

class GameClientService(GameService):
    def __init__(self, grid_columns, grid_rows, host_ip,
        server_port):
        self.__host_ip = host_ip
        self.__server_port = server_port
        GameService.__init__(self, grid_columns, grid_rows)

        self.__connected = False
        self._active = False
        self._player_index = -1
        self.__started = False
        self.__server_update_interval = 1
        self.__last_server_update_time = 0

        self.__update_commands = {
            "start": self.start,
            "activate": self.activate,
        }

    def update(self):
        if self.__connected == False:
            self.connect()
        else:
            self.handleConnection()
            if self.__started:
                GameService.update(self)

    def _placePiece(self, index):
        GameService._placePiece(self, index)
        if index == self._player_index:
            self.endTurn()

    def _getPieceToSpawn(self):
        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))

        self.__client.sendall(("spawn_piece " +
            str(self._player_index)).encode())
        piece_index = int(self.__client.recv(1024).decode())

        return piece_index

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
            str(self._player_index)).encode())
        update_response = self.__client.recv(1024).decode()

        self.handleUpdate(update_response)

        self.__last_server_update_time = time.clock()
    
    def requestPlayersNumber(self):
        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))

        self.__client.sendall(("players_number").encode())
        response = self.__client.recv(1024).decode()

        return int(response)


    def sendAction(self, string):
        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))
        self.__client.sendall(("announce_action " + string).\
            encode())

        response = self.__client.recv(1024).decode()

    def handleUpdate(self, update_response):
        parts = update_response.split(";")

        for update_part in parts:
            if len(update_part) > 0:
                command_parts = update_part.split()

                command = command_parts[0]

                if command in self.__update_commands:
                    self.__update_commands[command]()
                elif command in self._actions:
                    self.handleAction(update_part)
                elif command == "spawn":
                    piece_index = int(command_parts[1])
                    controller_index = int(command_parts[2])
                    self._spawnControlledPiece(piece_index,
                        controller_index)
                elif command != "none":
                    print("Invalid update command: " + command)

    def handleAction(self, string):
        action_player = int(string.split()[1])
        if self._active and\
            action_player == self._player_index:
            self.sendAction(string)

        GameService.handleAction(self, string)

    def connect(self):
        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))

        self.__client.sendall("connect".encode())
        recieved = self.__client.recv(1024).decode()
        self._player_index = int(recieved)
        self.__connected = True

    def start(self):
        GameService._startGravity(self)

        players_number = self.requestPlayersNumber()

        for _ in range(players_number - 1):
            self._controlled_pieces.append(None)
            self._score.append(0)
            self._soft_drop_cells.append(0)
            self._hard_drop_cells.append(0)

        self.__started = True

    def activate(self):
        self._active = True

    def endTurn(self):
        self._active = False

        self.__client = socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)
        self.__client.connect((self.__host_ip,
            self.__server_port))

        self.__client.sendall(("end_turn " +
            str(self._player_index)).encode())
        response = self.__client.recv(1024)
