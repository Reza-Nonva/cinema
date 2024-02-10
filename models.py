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

screen = Screen(DB_obj.connection, DB_obj.cursor)
# screen.show_screening(user.user)
# screen.set_movie_screening(1, '2024-02-06 20:00:00', '2024-02-06 21:30:00', 100)

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

    def add_card_by_user(self, user, card_number, date, cvv2, password):
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

    def deposite_withdraw_wallet(self, user_id, card_number, cvv2, password, pay_type, amount):
        user_card = self.cursor.execute("SELECT * FROM card_bank WHERE user_id = %s AND number = %s AND cvv = %s AND password = %s", (user_id, card_number, cvv2, password))
        user_card = self.cursor.fetchone()

        if user_card:
            print(self.wallet_balance(user_id))
            print(amount)
            if pay_type == 0:
                if self.wallet_balance(user_id) - amount < 0:
                    return False
                else:
                    amount = -amount
            
            
            payment_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pay_hash = utils.payment_code_hash()

            with open('log.transaction', 'a') as f:
                f.write(f"transiction in wallet, user_id={user_id},amount={amount},pay_date={payment_time}\n")

            self.cursor.execute(f"UPDATE wallet SET balance = balance + {amount} WHERE user_id = {user_id};")
            self.cursor.execute(f"INSERT INTO wallet_transaction(amount, payment_code, card_id, date, pay_type, user_id) VALUES ({amount}, {pay_hash}, {card_number}, '{payment_time}', {pay_type}, {user_id});")
            self.connection.commit()
            return True
        else:
            return False
 
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
    
accounting = Accounting(connection=DB_obj.connection, cursor=DB_obj.cursor)
# accounting.add_card_by_user(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765')
# accounting.initial_setup_wallet(user=user.user['id'])
# accounting.charge_wallet(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765', amount='110')
# accounting.charge_wallet(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765', amount='120000')
# print(accounting.wallet_balance(user=user.user['id']))
# buying plan by user
# accounting.initial_plan_mode(user=user.user['id'])
# accounting.buy_plan(user=user.user['id'], plan_name='silver')

class Ticket:
    '''
        This is a ticket class
    '''
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def buy_ticket(self, user:User, screen_id:int, chair_number:int):
        '''
            buying a ticket
        '''
        if not user :
            print("Error: User should be logged in first.")
            return
        
        self.cursor.execute(f"SELECT id FROM ticket WHERE chair_number = {chair_number}")
        is_chair_alreay_booked = self.cursor.fetchone()

        if is_chair_alreay_booked:
            print('Error: this chair is already booked plases reserve another')
            return

        if chair_number > 50 or chair_number < 1:
            print("Error : Chair number is out of range")
            return

        self.cursor.execute(f"""SELECT id, age_range
                               FROM movie
                               WHERE id = (SELECT movie_id
                                           FROM screening 
                                           WHERE id = {screen_id});""")
        movie_data= self.cursor.fetchone()
        
        self.cursor.execute(f"SELECT price FROM screening WHERE id = {screen_id} AND start_time > NOW();")
        screen_price = self.cursor.fetchone()

        if not screen_price:
            print('Error : Screen start time has passed.')
            return

        if not movie_data:
            print('Error : Movie has not found.')
            return

        age = datetime.now().date().year - user.user['birthdate'].year 

        if (movie_data[1] > age):
            print("Error : This movie is not suit for you.")
            return
    
        self.cursor.execute(f"SELECT number, cvv, password FROM card_bank where user_id = {user.user['id']}")
        card_data = self.cursor.fetchone()

        if not card_data:
            print(f'Error : User has no bank card')
            return

        transition = Accounting(connection=self.connection, cursor=self.cursor)
        if transition.deposite_withdraw_wallet(user.user['id'], card_data[0], card_data[1], card_data[2], 0, screen_price[0]):

            ticket_query = "INSERT INTO ticket (user_id ,screen_id ,chair_number) VALUES (%s, %s, %s)"
            ticket_data = (
                user.user['id'],
                screen_id,
                chair_number,
            )
            self.cursor.execute(ticket_query, ticket_data)
            self.connection.commit()

            print(f"you bought a ticket with for {user.user['username']} in chair number {chair_number}.")

        else:
            print('Error : card have not found or low cash')

        return

    def show_available_chairs(self, screen_id):
        self.cursor.execute(f'SELECT chair_number FROM ticket WHERE screen_id = {screen_id}')
        empty_chairs = self.cursor.fetchall()

        if not empty_chairs:
            print('Error : this screen id doesn\'t exist')
            return
        
        booked_chairs = set(num[0] for num in empty_chairs)
        free_chairs = [num for num in range(1, 51) if num not in booked_chairs]
        print(f'list of free chairs in {screen_id} screen : {free_chairs}')
        return
    
    def cancel_ticket(self, ticket_id):
        self.cursor.execute(f'SELECT user_id, screen_id, chair_number FROM ticket WHERE id = {ticket_id}')
        ticket_data = self.cursor.fetchone()

        if not ticket_data:
            print('Error : Ticket with this id have not found')
            return
        
        self.cursor.execute(f'SELECT price, start_time FROM screening WHERE id = {ticket_data[1]} AND start_time > NOW()')
        screen_data = self.cursor.fetchone()

        if not screen_data:
            print('Error : This screen has already started')
            return
        
        self.cursor.execute(f'SELECT number, cvv, password FROM card_bank where user_id = {ticket_data[0]}')
        card_data = self.cursor.fetchone()

        if not card_data:
            print(f'Error : User has no bank card')
            return

        price = screen_data[0] if screen_data[1] - datetime.now() > timedelta(hours=1) else screen_data[0] / 100 * 82
        accounting = Accounting(DB_obj.connection, DB_obj.cursor)
        if accounting.deposite_withdraw_wallet(ticket_data[0], card_data[0], card_data[1], card_data[2], 1, price):
            print(f'Ticket with has canceled and money returend to your card with {card_data[0]}')
            self.cursor.execute(f'DELETE FROM ticket WHERE id = {ticket_id}')
            self.connection.commit()
        else:
            print('card is invalid')

        return

ticket = Ticket(DB_obj.connection, DB_obj.cursor)
ticket.buy_ticket(user, 9, 41)
# ticket.show_available_chairs(9)
# ticket.cancel_ticket(2)


class Movie_Rate:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def rate_movie(self, user_id, movie_id, rating):
        # Validate the rating
        if not (1 <= rating <= 5):
            print("Error: Rate should be between 1 and 5")
            return

        # Check the user exists
        user_check_query = "SELECT id FROM users WHERE id = %s"
        self.cursor.execute(user_check_query, (user_id,))
        user_exists = self.cursor.fetchone()

        if not user_exists:
            print(f"Error: User with id {user_id} does not exist.")
            return

        # Check if the movie exists
        movie_check_query = "SELECT id FROM movies WHERE id = %s"
        self.cursor.execute(movie_check_query, (movie_id,))
        movie_exists = self.cursor.fetchone()

        if not movie_exists:
            print(f"Error: Movie with id {movie_id} does not exist.")
            return

        # Check if the user has already rated the movie
        check_query = "SELECT id FROM rank WHERE user_id = %s AND movie_id = %s"
        self.cursor.execute(check_query, (user_id, movie_id))
        existing_rank = self.cursor.fetchone()

        if existing_rank:
            print("Error: You have already rated this movie.")
            return

        # Insert the new rating
        insert_query = ("INSERT INTO rank (USER_ID, MOVIE_ID, RATING)"
                        " VALUES (%s, %s, %s)")

        rank_data = (
            user_id,
            movie_id,
            rating
        )
        self.cursor.execute(insert_query, rank_data)
        self.connection.commit()
        print(f"Rating added: {rating} star for movie {movie_id} by User {user_id}")

    def calculate_average_rating(self, movie_id):
        movie_check_query = "SELECT id FROM movies WHERE id = %s"
        self.cursor.execute(movie_check_query, (movie_id,))
        movie_exists = self.cursor.fetchone()

        if not movie_exists:
            print(f"Error: Movie with id {movie_id} does not exist.")
            return None

        # Calculate the average rating for the movie
        average_query = "SELECT AVG(rating) FROM rank WHERE movie_id = %s"
        self.cursor.execute(average_query, (movie_id,))
        average_rating = self.cursor.fetchone()[0]
        return average_rating

    def top_rated_movies(self, num_movies=10):
        # Retrieve the top-rated movies based on average ratings
        top_rated_query = """
            SELECT movies.id, AVG(rank.rating) as average_rating
            FROM movies
            JOIN rank ON movies.id = rank.movie_id
            GROUP BY rank.movie_id, movies.id
            ORDER BY average_rating DESC
            LIMIT %s
        """
        self.cursor.execute(top_rated_query, (num_movies,))
        top_rated_movies = self.cursor.fetchall()

        return top_rated_movies

    def get_movie_screenings(self, movie_id):
        # Retrieve the number of screenings for a specific movie
        movie_screenings_query = """
            SELECT COUNT(*) as num_screenings
            FROM screening
            WHERE movie_id = %s
        """

        self.cursor.execute(movie_screenings_query, (movie_id,))
        num_movie_screenings = self.cursor.fetchone()[0]
        return num_movie_screenings

    def write_comment(self, user_id, movie_id, comment_text, parent_comment_id=None):
        # Create comment
        insert_comment_query = """
            INSERT INTO comments (user_id, movie_id, parent_comment_id, comment_text, create_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        comment_data = (
            user_id, movie_id, parent_comment_id, comment_text, datetime.now()
        )
        self.cursor.execute(insert_comment_query, comment_data)
        self.connection.commit()

        # Create a reply if the comment is a reply to an original comment
        if parent_comment_id:
            insert_reply_query = """
                INSERT INTO replies (comment_id, user_id, reply_text, create_date)
                VALUES (%s, %s, %s, %s)
            """
            reply_data = (
                parent_comment_id, user_id, comment_text, datetime.now()
            )
            self.cursor.execute(insert_reply_query, reply_data)
            self.connection.commit()

        print("Comment sent successfully.")