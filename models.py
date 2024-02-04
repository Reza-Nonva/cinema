import mysql.connector
from datetime import datetime
import utils

class DBconnection:

    def __init__(self, host:str, port:int, user:str, password:str, database:str):
            
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
    
        self.cursor = self.connection.cursor()
        self.create_table()


    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            mobile_number VARCHAR(11),
            birthdate DATE NOT NULL,
            register_date DATE NOT NULL,
            last_login_date DATE NOT NULL,
            last_login_time TIME NOT NULL
        )
        """

        self.cursor.execute(create_table_query)
        self.connection.commit()
    


class User:
    def __init__(self):
        
        self.isAuthenticated = False
        self.user = None

    def register_user(self, connection, cursor, username:str, password:str, email:str, birthdate:str, mobile_number:str=None):

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_username = cursor.fetchone()

        if existing_username:
            print(f"Error: Username '{username}' is already taken. Please choose a different username.")
            return

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            print(f"Error: Email '{email}' is already used. Please choose a different email.")
            return
        
        if not utils.validating_email(email):
            print(f"Error: Email '{email}' is not a valid email. Please use a different email.")
            return

        if not utils.validating_username(username):
            print("Error: Username should contain both uppercase and lowercase word . Please use a different username.")
            return
    
        if not utils.validating_password(password):
            print("Error: Password should be mpre than 8 character and contain uppercase, lowercase, number and spercial signs . Please use a different password.")
            return

        if not utils.validating_mobile_number(mobile_number):
            print(f"Error: Mobile Mumber '{mobile_number}' is not a valid email. Please use a different mobile number.")
            return

        insert_query = """
            INSERT INTO users (username, password, email, mobile_number, birthdate, register_date, last_login_date, last_login_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        user_data = (
            username,
            utils.hash_password(password),
            email,
            mobile_number,
            birthdate,
            datetime.now().date(),
            datetime.now().date(),
            datetime.now().time(),
        )

        cursor.execute(insert_query, user_data)
        connection.commit()

        self.login_user(connection, cursor, username, password)

    def login_user(self, connection, cursor, username, password):
        if self.isAuthenticated:
            print('You already logged in please logout first')
            return
        
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, utils.hash_password(password)))
        user_obj = cursor.fetchone()

        if not user_obj:
            print('Authentication failed. password or email may be wrong')
            return
                
        columns = [column[0] for column in cursor.description]
        self.user = dict(zip(columns, user_obj))

        self.isAuthenticated = True

        cursor.execute("UPDATE users SET last_login_time = %s WHERE id = %s", (datetime.now().time() ,self.user['id']))
        connection.commit()
        print(f"Dear {self.user['username']} you have just logged in")
        return

    def change_profile(self):
        pass

    def change_password(self):
        pass

    def logout(self):
        self.isAuthenticated = False
        self.user = None


DB_obj = DBconnection('tai.liara.cloud', 33428, 'root', 'ErOmibw13imQzlzw3TIgyE10', 'focused_driscoll')
user = User()

user.register_user(DB_obj.connection, DB_obj.cursor, 'Bagher5', 'Thisis@p@ssword1', 'palahangmohammadbagher5@gmail.com', '1382-06-01', '0902341014')
# user.login_user(DB_obj.connection, DB_obj.cursor, 'ali', 'fuckyou2')
