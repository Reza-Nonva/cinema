import mysql.connector
from datetime import datetime
import utils


class User:
    def __init__(self, host:str, port:int, user:str, password:str, database:str):
        
        self.isAuthenticated = False
        self.user_id = None

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

    def register_user(self, username:str, password:str, email:str, birthdate:str, mobile_number:int=None):

        self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_username = self.cursor.fetchone()

        #  TODO: Validating username, email, password, phone number,

        if existing_username:
            print(f"Error: Username '{username}' is already taken. Please choose a different username.")
            return

        self.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_email = self.cursor.fetchone()

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
            print("Error: Password should be mpre than 8 character and contain uppercase, lowercase, number and spercial signs . Please use a different username.")
            return

        if not utils.validating_mobile_number(mobile_number):
            print(f"Error: Mobile Mumber '{mobile_number}' is not a valid email. Please use a different email.")
            return



        insert_query = """
            INSERT INTO users (username, password, email, mobile_number, birthdate, register_date, last_login_date, last_login_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        user_data = (
            username,
            password,
            email,
            mobile_number,
            birthdate,
            datetime.now().date(),
            datetime.now().date(),
            '10:23'

        )

        self.cursor.execute(insert_query, user_data)
        self.connection.commit()

        self.login_user(username, password)

    def login_user(self, username, password):
        if self.isAuthenticated:
            print('You already logged in please logout first')
            return
        
        self.cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = self.cursor.fetchone()

        if not user:
            print('Authentication failed. password or email may be wrong')
            return
        
        self.isAuthenticated = True
        self.user_id = user[0]
        print(type(user[0]))
        print(f'Dear {self.user_id} you have just logged in')
        return


    def logout(self):
        self.isAuthenticated = False
        self.user = None


user = User('tai.liara.cloud', 33428, 'root', 'ErOmibw13imQzlzw3TIgyE10', 'focused_driscoll')
# user.register_user('bagher', 'fuckyou2', 'palahangmohammadbagher@gmail.com', '2020-04-04', '09023241014')
# user.login_user('bagher', 'fuckyou2')
# print(user.isAuthenticated)