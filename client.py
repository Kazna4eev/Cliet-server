import socket
import threading

class ClientChat:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.nickname = input('Enter your nickname: ')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect((self.host, self.port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print('An error occurred!')
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}\n'
            self.client.send(message.encode('utf-8'))

if __name__ == '__main__':
    client = ClientChat()
    client.connect()

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    write_thread = threading.Thread(target=client.write)
    write_thread.start()
