import socket
import threading
import models
from db import DB_obj
import argparse


menu = """ ====User Menu====
+change_profile [username or email or mobile_number] [new value]         
+change_password [old password] [new password] [confirm new password]
+show_screening_movie
+add_card [card number] [date] [cvv2] [password]
+charge_wallet [card nummber] [amout]
+show_available_chairs [screen id]
+buy_ticket [screen id] [chair number]
+cancel_ticket [ticket id]
+rate_movie [movie id] [rating]
+avg_rate [movie id]
+top_rated_movies [count]
+count_screening [movie id]
+logout
+dis """
    
admin_menu = """ ====Admin Menu=====
+change_profile [username or email or mobile_number] [new value]         
+change_password [old password] [new password] [confirm new password]
+show_screening_movie
+add_card [card number] [date] [cvv2] [password]
+charge_wallet [card nummber] [amout]
+show_available_chairs [screen id]
+buy_ticket [screen id] [chair number]
+cancel_ticket [ticket id]
+add_movie [name] [year] [age range]
+list_movie
+add_screen [movie id] [start time(y-m-d h-m-s)] [end time(y-m-d h-m-s)] [price]
+rate_movie [movie id] [rating]
+avg_rate [movie id]
+top_rated_movies [count]
+count_screening [movie id]
+logout
+dis
"""
welcome_message = """you must login or register first
>+login [username] [password]
>+register [username] [password] [email] [birthdate] [mobile number]
"""

FORMAT = 'UTF-8' 

def handle_request(user, msg:str):
    #TODO: 1. user can edit just once of profile information
    msg = msg.split()
    global menu    
    global admin_menu
    global welcome_message
    match msg[0]:
        case "menu":
            if user.isAuthenticated :
                if user.user["is_admin"] == 1:
                    return(admin_menu)
                else:
                    return(menu)
            else:
                return(welcome_message)
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
        case "change_password":
            return(user.change_password(old_password=msg[1], new_password=msg[2], new_password_confirm=msg[3]))
        
        case "show_screening_movie":
            screen = models.Screen(DB_obj.connection, DB_obj.cursor)
            return(screen.show_screening(user=user))
        
        case "add_card":
            accounting = models.Accounting(DB_obj.connection, DB_obj.cursor)
            
            user_id = user.user
            if user_id is None:
                return("please login first")
            return (accounting.add_card_by_user(user = user_id["uuid"], card_number=msg[1], date=msg[2], cvv2=int(msg[3]), password = int(msg[4])))
        
        case "charge_wallet":
            return(user.charge_wallet(msg[1], msg[2]))
        
        case "show_available_chairs":
            ticket = models.Ticket(DB_obj.connection, DB_obj.cursor)
            return (ticket.show_available_chairs(int(msg[1])))
        
        case "buy_ticket":
            ticket = models.Ticket(DB_obj.connection, DB_obj.cursor)
            return(ticket.buy_ticket(user, int(msg[1]), int(msg[2])))
        
        case "cancel_ticket":
            ticket = models.Ticket(DB_obj.connection, DB_obj.cursor)
            return(ticket.cancel_ticket(user, int(msg[1])))

        case "add_movie":
            movie = models.Movie(DB_obj.connection, DB_obj.cursor)
            return(movie.add_movie(user, msg[1], int(msg[2]), int(msg[3])))
        
        case "list_movie":
            movie = models.Movie(DB_obj.connection, DB_obj.cursor)
            return(movie.list_of_movie(user = user))
        
        case "add_screen":
            screen = models.Screen(DB_obj.connection, DB_obj.cursor)
            return(screen.set_movie_screening(user= user, movie_id=int(msg[1]), start_time=msg[2]+" "+msg[3],end_time=msg[4] + " " +msg[5], price=int(msg[6])))
        case "rate_movie":
            movie_rate = models.Movie_Rate(DB_obj.connection, DB_obj.cursor)
            return(movie_rate.rate_movie(user, int(msg[1]), int(msg[2])))
        
        case "avg_rate":
            movie_rate = models.Movie_Rate(DB_obj.connection, DB_obj.cursor)
            return(movie_rate.calculate_average_rating(int(msg[1])))


        case "top_rated_movies":
            movie_rate = models.Movie_Rate(DB_obj.connection, DB_obj.cursor)
            return(movie_rate.top_rated_movies(int(msg[1])))
        
        case "count_screening":
            movie_rate = models.Movie_Rate(DB_obj.connection, DB_obj.cursor)
            return(movie_rate.get_movie_screenings(int(msg[1])))
        case "logout":
            return(user.logout())
        
        
        case _:
            return("invalid command, run menu to see commands")
    
def handle_client(conn, addr):
    global FORMAT
    DISCONNECT_MESSAGE = "!DISCONNECT"
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

def create_admin():
    username = input("username: ")
    password = input("password: ")
    email = input("email: ")
    birthdate = input("birthdate(y-m-d): ")
    mobile_number = input("mobile number: ")
    user = models.User(DB_obj.connection, DB_obj.cursor)
    return(user.register_user(username=username, password=password, email=email, birthdate=birthdate, mobile_number= mobile_number, is_admin=1))


def start():
    global FORMAT
    HEADER = 1024
    PORT = 12345
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
       
    

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    
    server.listen()
    
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

parser = argparse.ArgumentParser()
parser.add_argument('--createadmin', action="store_true")
if(parser.parse_args().createadmin): 
    print(create_admin())
else:
    print("[STARTING] server is starting...")
    start()