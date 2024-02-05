from datetime import datetime
from db import DB_obj
import utils

class User:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.isAuthenticated = False
        self.user = None

    def register_user(self, username:str, password:str, email:str, birthdate:str, mobile_number:str=None):

        self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_username = self.cursor.fetchone()

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

        self.cursor.execute(insert_query, user_data)
        self.connection.commit()

        self.login_user(username, password)

    def login_user(self, username, password):
        if self.isAuthenticated:
            print('You already logged in please logout first')
            return
        
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, utils.hash_password(password)))
        user_obj = self.cursor.fetchone()

        if not user_obj:
            print('Authentication failed. password or email may be wrong')
            return
                
        columns = [column[0] for column in self.cursor.description]
        self.user = dict(zip(columns, user_obj))

        self.isAuthenticated = True

        self.cursor.execute("UPDATE users SET last_login_time = %s WHERE id = %s", (datetime.now().time() ,self.user['id']))
        self.connection.commit()
        print(f"Dear {self.user['username']} you have just logged in")
        return

    def change_profile(self, username=None, email=None, mobile_number=None):
        if not self.isAuthenticated:
            print("Error: User should be logged in first.")
            return
        
        if username:
            self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            existing_username = self.cursor.fetchone()

            if existing_username:
                print(f"Error: Username '{username}' is already taken. Please choose a different username.")
            else:
                if utils.validating_username(username):
                    self.cursor.execute("UPDATE users SET username = %s WHERE id = %s", (username, self.user['id']))
                    print(f"Dear {self.user['username']} you have just change your username")
                else:
                    print("Error: Username should contain both uppercase and lowercase word . Please use a different username.")

        if email:
            self.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_email = self.cursor.fetchone()

            if existing_email:
                print(f"Error: Email '{email}' is already taken. Please choose a different email.")
            else:
                if utils.validating_email(email):
                    self.cursor.execute("UPDATE users SET email = %s WHERE id = %s", (email, self.user['id']))
                    print(f"Dear {self.user['username']} you have just change your email")
                else:
                    print(f"Error: Email '{email}' is not a valid email. Please use a different email.")

        if mobile_number:
            if utils.validating_mobile_number(mobile_number):
                self.cursor.execute("UPDATE users SET email = %s WHERE id = %s", (email, self.user['id']))
                print(f"Dear {self.user['username']} you have just change your mobile number")
            else:
                print(f"Error: Mobile Mumber '{mobile_number}' is not a valid email. Please use a different mobile number.")

        self.connection.commit()


    def change_password(self, old_password, new_password, new_password_confirm):
        if not self.isAuthenticated:
            print("Error: User should be logged in first.")
            return

        if new_password != new_password_confirm:
            print("Error: new_password and new_password_confirm should be the same.")
            return
        
        if not utils.validating_password(new_password):
            print("Error: Password should be mpre than 8 character and contain uppercase, lowercase, number and spercial signs . Please use a different password.")
            return

        self.cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (self.user['username'], utils.hash_password(old_password)))
        user_id = self.cursor.fetchone()

        if not user_id:
            print('Error: username or old password is incorrect. please check and fill again.')
            return
        
        self.cursor.execute("UPDATE users SET password = %s WHERE id = %s", (utils.hash_password(new_password), self.user['id']))
        self.connection.commit()

        print(f"Dear {self.user['username']} you have just change your password")
        return

    def logout(self):
        self.isAuthenticated = False
        self.user = None

    def __str__(self):
        if not user.isAuthenticated:
            print('You are not logged in')
            return
        print(self.user['username'])

user = User(DB_obj.connection, DB_obj.cursor)
# user.register_user('Bagher6', 'Thisis@p@ssword1', 'palahangmohammadbagher6@gmail.com', '1382-06-01', '09023241014')
user.login_user('ali', 'Thisis@p@ssword1')
# user.change_password('Thisis@p@ssword1', 'Thisis@p@ssword2', 'Thisis@p@ssword2')
user.login_user('Alireza1', 'Thisis@p@ssword2')
user.change_profile(username='Alireza2', email='fuck@thefucking.world')

class Movie:
    name:str
    year:int
    age_range:int
    def __init__():
        pass
    
    
    def add_movie(self, connection, cursor, name, year, age_range):
        self.name = name
        self.year = year
        self.age_range = age_range
        cursor.execute("SELECT id FROM movie WHERE name = %s", (self.name))
        existing_movie = cursor.fetchone()
        if existing_movie:
            print(f"Error: Movie '{Movie}' is already added.")
            return
        insert_query = "INSERT INTO movie (name, year, age_range) VALUES ((%s, %s, %s))",(self.name, self.year, self.age_range)