import socket
import pickle
from threading import Thread


def send(skt: socket.socket, msg):
    data = pickle.dumps(msg)
    skt.send(data)


def recv(skt: socket.socket):
    data = skt.recv(BUFSIZ)
    return pickle.loads(data)


def accept_incoming_connections(server: socket.socket):
    while True:
        client, address = server.accept()
        print(f'connected to {address}')
        addresses[client] = address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client: socket.socket):
    msg = 'Welcome to the chat group please enter you name first'
    data = send(client, msg)
    name = recv(client)
    clients[client] = name
    msg = f'Welcome {name} type message and press button to send it you can exit by sending quit'
    send(client, msg)
    msg = f'{name} joined the chat'
    broadcast(msg)
    while True:
        msg = recv(client)
        if msg != 'quit':
            broadcast(msg, name)
        else:
            msg = 'left the chat'
            broadcast(msg, name)
            del clients[client]
            client.close()
            break


def broadcast(msg, name=''):
    if name:
        msg = f'{name}: {msg}'
    data = pickle.dumps(msg)
    for client in clients:
        client.send(data)


HOST = ''
PORT = 8200
ADDR = (HOST, PORT)
BUFSIZ = 1024
MAX_CLIENTS = 5
clients = {}
addresses = {}


def main():
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(MAX_CLIENTS)
    print('Waiting for connections...')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    

if __name__ == '__main__':
    main()