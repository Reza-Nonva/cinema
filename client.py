import socket
import threading

HEADER = 1024
PORT = 12345
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)

def receive():
    while True:
        try:
            msg = client.recv(HEADER).decode(FORMAT)
            if msg:
                print(msg)
        except Exception as e:
            print(f"Error: {e}")
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()
print("enter menu to see menu")
while (True):
    data = input()
    if (data == "dis"):
        print("good bye")
        send(DISCONNECT_MESSAGE)
        break
    else:
        send(data)
