import socket
import pickle
from threading import Thread
import PyQt5.QtWidgets as q
from PyQt5.QtCore import QObject, pyqtSignal
import sys


def send(skt: socket.socket, data):
    data = pickle.dumps(data)
    skt.send(data)


def recv(skt: socket.socket):
    data = skt.recv(BUFSIZ)
    return pickle.loads(data)


def receive_thread(signal):
    while RUN:
        msg = recv(skt)
        CHAT_HISTORY.append(msg)
        signal.rcvd_data.emit()


class Communicate(QObject):
    rcvd_data = pyqtSignal()


class MyWindow(q.QWidget):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal
        self.initUI()
    
    def initUI(self):
        self.chatBox = q.QTextBrowser(self)
        self.msgPanel = q.QTextEdit(self)
        self.sendButton = q.QPushButton('Send', self)
        self.sendButton.clicked.connect(self.send_button)
        self.signal.rcvd_data.connect(self.update_chatbox)

        self.vbox = q.QVBoxLayout(self)
        self.vbox.addWidget(self.chatBox)
        self.vbox.addWidget(self.sendButton)
        self.vbox.addWidget(self.msgPanel)

        self.setGeometry(0,0,500,500)
        self.setWindowTitle('chat')
        self.show()
    
    def send_button(self):
        text = self.msgPanel.toPlainText()
        send(skt, text)
        self.msgPanel.clear()
    
    def update_chatbox(self):
        self.chatBox.setText('\n'.join(CHAT_HISTORY))


RUN = True
HOST = '127.0.0.1'
PORT = 8200
ADDR = HOST, PORT
BUFSIZ = 1024
CHAT_HISTORY = []
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.connect(ADDR)

def main():
    app = q.QApplication(sys.argv)
    signal = Communicate()
    win = MyWindow(signal)
    Thread(target=receive_thread, args=(signal,)).start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()