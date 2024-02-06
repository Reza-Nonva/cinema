from datetime import datetime, timedelta
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
# user.login_user('ali', 'Thisis@p@ssword1')
# user.change_password('Thisis@p@ssword1', 'Thisis@p@ssword2', 'Thisis@p@ssword2')
user.login_user('Alireza2', 'Thisis@p@ssword2')
# user.change_profile(username='Alireza2', email='fuck@thefucking.world')


class Movie:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add_movie(self, name:str, year:int, age_range:int):
        self.name = name
        self.year = year
        self.age_range = age_range

        self.cursor.execute("SELECT id FROM movie WHERE name = %s", (self.name,))
        existing_movie = self.cursor.fetchone()

        if existing_movie:
            print(f"Error: Movie '{Movie}' is already added.")
            return

        insert_query = """
            INSERT INTO movie (name, year, age_range) VALUES (%s, %s, %s)
        """
        movie_data = (name, year, age_range)
        self.cursor.execute(insert_query, movie_data)
        self.connection.commit()
        print(f"Movie '{name}' added")
        return 
    

movie = Movie(DB_obj.connection, DB_obj.cursor)
# movie.add_movie('inception', 2016, 18)


class Screen:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def show_screening(self, user):
        if not user :
            print("Error: User should be logged in first.")
            return
        
        self.cursor.execute(f"SELECT * FROM screening WHERE start_time > NOW();")
        result = self.cursor.fetchall()

        columns = [column[0] for column in self.cursor.description]
        for row in result:
            screening = dict(zip(columns, row))
            self.cursor.execute("SELECT name FROM movie WHERE id = %s",(screening['movie_id'],))
            result = self.cursor.fetchone()

            print(f"{screening['id']} ---> name:{result[0]} -- price:{screening['price']} -- start:{screening['start_time']} -- duration:{screening['end_time']-screening['start_time']}")

    def set_movie_screening(self, movie_id, start_time, end_time, price):
        if not user:
            print("Error: User should be logged in first.")
            return
        
        self.cursor.execute("SELECT name FROM movie WHERE id = %s",(movie_id,))
        movie_exist = self.cursor.fetchone()
        
        if not movie_exist:
            print('Error : Movie has not declared')
            return

        insert_query = """
            INSERT INTO screening (movie_id, start_time, end_time, price) VALUES (%s, %s, %s, %s)
        """

        screening_data = (
            movie_id,
            start_time,
            end_time,
            price
        )

        self.cursor.execute(insert_query, screening_data)
        self.connection.commit()
        print(f'{movie_exist[0]} added to screen start time : {start_time}')


    def reserve_screen(self, user, screen_id):
        if not user :
            print("Error: User should be logged in first.")
            return
        self.cursor.execute(f"""SELECT id, age_range
                               FROM movie
                               WHERE id = (SELECT movie_id
                                           FROM screening 
                                           WHERE id = {screen_id})""")
        movie_data= self.cursor.fetchone()
        if (movie_data[1] > user.user['age']):
            print("Age limit, boro bozorg shodi bia")
            return
        buy_screen = Accounting(connection=self.connection, cursor=self.cursor)
        buy_screen.buy_screen(user = user, movie = movie_data[0], screen_id = screen_id)
        print("ok")
        
        
        
# screen = Screen(DB_obj.connection, DB_obj.cursor)    
# screen.show_screening(user.user)
# screen.set_movie_screening(1, '2024-02-06 20:00:00', '2024-02-06 21:30:00', 100)
>>>>>>>>> Temporary merge branch 2

class Accounting:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def initial_setup_wallet(self, user):
        self.cursor.execute(f"SELECT * FROM wallet WHERE user_id={user};")
        if self.cursor.fetchone():
            print('You already have a wallet')
            return
        else:
            self.cursor.execute(f"INSERT INTO wallet(user_id, balance) VALUES ({user}, 0);")
            self.connection.commit()

    def add_card_by_user(self, user, card_number, cvv2, date, password):
        if not utils.card_number_check(card_number):
            print(f'{card_number} is invalid card number')
            return
        
        self.cursor.execute(f"select number from card_bank where user_id ={user} and number={card_number};")
        user_cards = self.cursor.fetchone()
        if user_cards:
            print(f'{card_number} is already added')
        else:
            self.cursor.execute(f"INSERT INTO card_bank(user_id, number, cvv, date, password) VALUES ({user}, {card_number}, {cvv2}, {date}, {password});")
            self.connection.commit()
            print(f'{card_number} is added successfully')

    
    def charge_wallet(self, user, card_number, cvv2, date, password, amount=None):
        user_card = self.cursor.execute(f"select * from card_bank where user_id ={user} and number={card_number} and cvv={cvv2} and date={date} and password={password};")
        user_card = self.cursor.fetchone()
        if user_card:
            payment_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pay_hash = utils.payment_code_hash()
            with open('log.transaction', 'a') as f:
                f.write(f"charge wallet, user_id={user},amount={amount},pay_date={payment_time}\n")
            self.cursor.execute(f"UPDATE wallet SET balance = balance + {amount} WHERE user_id = {user};")
            self.cursor.execute(f"INSERT INTO wallet_transaction(payment_code, card_id, date, pay_type, user_id) VALUES ({pay_hash}, {card_number}, '{payment_time}', 1, {user});")
            self.connection.commit()
            print(f'{amount} added successfully your wallet')

        else:
            print(f"card data is invalid")


    def wallet_balance(self, user:int):
        balance = self.cursor.execute(f"SELECT balance from wallet WHERE user_id={user}")
        balance = self.cursor.fetchone()[0]
        self.connection.commit()
        return balance


    def initial_plan_mode(self, user:int):
        self.cursor.execute(f"SELECT * FROM wallet WHERE user_id={user};")
        if self.cursor.fetchone():
            print('You already have a basic plan')
            return
        else:
            self.cursor.execute(f"INSERT INTO plan(user_id, plan_id, start_time, finish_time) VALUES ({user}, {1}, '{datetime.now()}', '{datetime.now() + timedelta(days=31)}');")
            self.connection.commit()

    def buy_plan(self, user:int, plan_name):
        plan_price = {
            'bronze':[1, 10000],
            'silver': [2, 50000],
            'gold': [3, 100000],
        }
        
        self.cursor.execute(f"SELECT plan_id from plan where user_id = {user};")
        user_current_plan = self.cursor.fetchone()
        self.connection.commit()
        if self.wallet_balance(user) < plan_price[plan_name][1]:
            print('Your wallet balance is not enough')
        elif int(user_current_plan[0]) == plan_price[plan_name][0]:
            print('You already have this plan')
        else:
            payment_time = datetime.now()
            finish_time = datetime.now() + timedelta(days=31)
            pay_hash = utils.payment_code_hash()
            with open('log.transaction', 'a') as f:
                f.write(f"plan order: {plan_name}, user_id: {user}, price: {plan_price[plan_name][1]} from {payment_time} to {finish_time}, pay_hash: {pay_hash}\n")
            self.cursor.execute(f"INSERT INTO plan_transaction(plan_id, payment_code, date, user_id) VALUES ({plan_price[plan_name][0]}, {pay_hash}, '{payment_time}', {user});")
            self.cursor.execute(f"INSERT INTO plan(user_id, plan_id, start_time, finish_time) VALUES ({user}, {plan_price[plan_name][0]}, '{payment_time}', '{finish_time}');")
            self.cursor.execute(f"UPDATE wallet SET balance = balance - {plan_price[plan_name][1]} WHERE user_id={user};")
            self.connection.commit()
            print(f"The {plan_name} plan has been successfully purchased and the amount has been deducted from your wallet.")

    
    def buy_screen(self, user, movie:int, screen_id:int):
        screen_detail = self.cursor.execute(f"""
            SELECT name, year, start_time, end_time, screening.id, screening.price FROM screening
            LEFT JOIN movie
            ON screening.movie_id = movie.id
            WHERE movie.id={movie} and screening.id ={screen_id};
        """)
        screen_detail = self.cursor.fetchone()
        user_balance = self.cursor.execute(f"""
            SELECT wallet.balance FROM users
            LEFT JOIN wallet
            on users.id = wallet.user_id
            WHERE users.id={user};
        """)
        user_balance = self.cursor.fetchone() # wallet balance
        self.connection.commit()
        # print(f"movie: {screen_detail[0]}-{screen_detail[1]} in screen {screen_detail[4]} from {screen_detail[2].strftime('%Y-%m-%d %H:%M:%S')} to {screen_detail[3].strftime('%Y-%m-%d %H:%M:%S')}")
        # check has enough money in wallet for buy a ticket
        if screen_detail[5] > user_balance[0]:
            print("you don'y have enough money in your wallet, please first charge your wallet")
            return
        else:
            ticket_code = str(utils.payment_code_hash())[:10]
            with open('log.transaction', 'a') as f:
                f.write(f"plan order: {screen_detail[0]}, user_id: {user}, price: {screen_detail[5]} from ({screen_detail[2].strftime('%Y-%m-%d %H:%M:%S')} to {screen_detail[3].strftime('%Y-%m-%d %H:%M:%S')}), ticket_code: {ticket_code}\n")
            self.cursor.execute(f"UPDATE wallet SET balance = balance - {screen_detail[5]} WHERE user_id={user};")
            self.cursor.execute(f"INSERT INTO screen_transaction(screen_id, user_id, payment_code, buy_time) VALUES ({screen_detail[4]}, {user}, {ticket_code}, '{datetime.now()}');")
            self.connection.commit()
            print(f"Your ticket for movie {screen_detail[0]} ({screen_detail[2].strftime('%Y-%m-%d %H:%M:%S')} to {screen_detail[3].strftime('%Y-%m-%d %H:%M:%S')}) has been successfully purchased")
            print(f"your ticket number is {ticket_code}")
            

accounting = Accounting(connection=DB_obj.connection, cursor=DB_obj.cursor)
# accounting.add_card_by_user(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765')
# accounting.initial_setup_wallet(user=user.user['id'])
# accounting.charge_wallet(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765', amount='110')
# accounting.charge_wallet(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765', amount='120000')
# print(accounting.wallet_balance(user=user.user['id']))
# buying plan by user
# accounting.initial_plan_mode(user=user.user['id'])
# accounting.buy_plan(user=user.user['id'], plan_name='silver')
# accounting.buy_screen(user=user.user['id'], movie=1, screen_id=1)