import socket
import threading
import models
from db import DB_obj


HEADER = 1024
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

menu = """+register [username] [password] [email] [birthdate] [mobile number]
+login [username] [password] 
+change_profile [username or email or mobile_number] [new value]         
+logout
+dis """
    


def handle_request(user, msg:str):
    #TODO: 1. user can edit just once of profile information
    msg = msg.split()
    #print(msg)
    global menu    
    
    match msg[0]:
        case "menu":
            return (menu)
        case "register":
            return (user.register_user(username=msg[1], password=msg[2], email = msg[3], birthdate=msg[4], mobile_number=msg[5]))
        case "login":
            return(user.login_user(msg[1], msg[2]))
        case "change_profile":
            match msg[1]:
                case "username":
                    return (user.change_profile(username = msg[2]))
                case "email":
                    return (user.change_profile(email = msg[2]))  
                case "mobile_number":
                    return (user.change_profile(mobile_number = msg[2]))
        case "logout":
            return(user.logout())
        
    if msg[0] == "login":
        temp = user.login_user(msg[1], msg[2])
        return(temp)
    
    if msg[0] == "menu":
        return (menu)
    else:
        return ("ridi")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    user = models.User(DB_obj.connection, DB_obj.cursor)
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if msg:
            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue
            else:
                answer = handle_request(user, msg)
        conn.send(answer.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
