import socket
import threading
import os
from datetime import datetime

class ServerChat:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f'Server listening on {self.host}:{self.port}...')

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                nickname = self.nicknames[index]
                print(f'{nickname} has left the chat!')
                self.broadcast(f'{nickname} has left the chat!\n'.encode('utf-8'))
                self.nicknames.remove(nickname)
                client.close()
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            self.broadcast(f'{nickname} has joined the chat!\n'.encode('utf-8'))
            client.send('Connected to the server!\n'.encode('utf-8'))

            # create a new chat history file for the current session
            chat_history_dir = os.path.join(os.path.dirname(__file__), 'chat_history')
            os.makedirs(chat_history_dir, exist_ok=True)
            chat_history_file = f"chat_history_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            chat_history_path = os.path.join(chat_history_dir, chat_history_file)
            with open(chat_history_path, "w") as f:
                f.write(f"{nickname} has joined the chat!\n")

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def start(self):
        self.clients = []
        self.nicknames = []
        self.receive()

if __name__ == '__main__':
    server = ServerChat()
    server.start()
