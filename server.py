import socket
import pickle
from threading import Thread


def accept_incoming_connections(server: socket.socket):
    while True:
        conn, address = server.accept()
        print(f'connected to {address}')
        addresses[conn] = address
        Thread(target=handle_client, args=(conn,)).start()


def handle_client(client: socket.socket):
    msg = 'Welcome to the chat group please enter you name first'
    data = pickle.dumps(msg)
    client.send(data)
    


def broadcast(msg, name):
    data = pickle.dumps((msg, name))
    for addr in addresses:
        addr.send(data)


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