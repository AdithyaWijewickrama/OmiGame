import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!disconnect'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleclient(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected')
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            print(f'[{addr}] [{msg}]')
            if msg == DISCONNECT_MSG:
                connected = False

    conn.close_btn()


def start():
    server.listen()
    print(f'[LISTENING] Server is listening at {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleclient, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNS] {threading.active_count() - 1}')


print('[STARTING] server is starting')
start()
