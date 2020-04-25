import socket
import pickle
from threading import Thread


def accept_incoming_connections():
    while True:
        client, address = SERVER.accept()
        print(f'new client: {address}')
        msg = 'Welcome to the chat please enter your name'
        client.send(pickle.dumps(msg))
        addresses[client] = address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client: socket.socket):
    name = client.recv(BUFSIZ)
    name = pickle.loads(name)
    clients[client] = name
    # msg = f'Welcome {name} if you want to quit, type {{quit}} to exit'
    # client.send(pickle.dumps(msg))
    msg = f'{name} has joined the chat'
    broadcast(msg)
    while True:
        msg = client.recv(BUFSIZ)
        msg = pickle.loads(msg)
        if msg == 'quit':
            msg = f'{name} has left the chat'
            broadcast(msg)
            del clients[client]
            client.close()
            break
        else:
            broadcast(msg, name)


def broadcast(msg: str, name=''):
    for client in clients:
        data = pickle.dumps((name, msg))
        client.send(data)


HOST = ''
PORT = 8005
ADDR = (HOST, PORT)
BUFSIZ = 1024
MAX_CLIENTS = 5

clients = {}
addresses = {}

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == '__main__':
    SERVER.listen(MAX_CLIENTS)
    print('Waiting for connections...')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

