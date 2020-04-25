import socket
import pickle
import subprocess
from threading import Thread
import PyQt5.QtWidgets as q


def receive():
    while run:
        msg = connection.recv(BUFSIZ)
        name, msg = pickle.loads(msg)
        msg = f'{name}: {msg}' if name else msg
        CONVERSATION.extend(['', msg])
        print_text()


def print_text():
    subprocess.run('clear')
    for line in CONVERSATION:
        print(line)


def add_line(msg):
    CONVERSATION.extend(['', msg])


HOST = input('host: ')
PORT = int(input('port: '))

if not PORT:
    PORT = 8005

ADDR = (HOST, PORT)
BUFSIZ = 1024

CONVERSATION = []
run = True

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(ADDR)
msg = connection.recv(BUFSIZ)
msg = pickle.loads(msg)
print(msg)
msg = pickle.dumps(input('type name: '))
connection.send(msg)
receive_thread = Thread(target=receive)
receive_thread.start()
while True:
    msg = input()
    if msg == 'quit':
        connection.close()
        run = False
        break
    data = pickle.dumps(msg)
    connection.send(data)
    print_text()












