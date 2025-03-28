import socket


HEADER=64
PORT=5050
DISCONNECT_MSG='!disconnect'
FORMAT='utf-8'
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    massage=msg.encode(FORMAT)
    msg_len=len(massage)
    send_len=str(msg_len).encode(FORMAT)
    # b'' means to binary
    send_len+=b' '*(HEADER-len(send_len))
    client.send(send_len)
    client.send(massage)

send('hello fucker')