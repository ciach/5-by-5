# game_server.py

import socket


class GameServer:
    def __init__(self, host="127.0.0.1", port=65432):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        print(f"Server started. Waiting for players to connect on {host}:{port}...")

    def run(self):
        player1, addr1 = self.server_socket.accept()
        print(f"Player 1 connected from {addr1}")
        player1.sendall(b"Welcome Player 1")

        player2, addr2 = self.server_socket.accept()
        print(f"Player 2 connected from {addr2}")
        player2.sendall(b"Welcome Player 2")

        # Main game loop (placeholder)
        while True:
            data = player1.recv(1024)
            if not data:
                break
            print(f"Received from Player 1: {data.decode()}")
            player2.sendall(data)

            data = player2.recv(1024)
            if not data:
                break
            print(f"Received from Player 2: {data.decode()}")
            player1.sendall(data)

        player1.close()
        player2.close()


if __name__ == "__main__":
    server = GameServer()
    server.run()
