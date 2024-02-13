from datetime import datetime, timedelta
from db import DB_obj
import utils

def login_required():
    pass

class Accounting:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def initial_setup_wallet(self, user):
        self.cursor.execute(f"SELECT * FROM wallet WHERE user_id='{user}';")
        if self.cursor.fetchone():
            return('You already have a wallet')
        else:
            self.cursor.execute(f"INSERT INTO wallet(user_id, balance) VALUES ('{user}', 0);")
            self.connection.commit()

    def add_card_by_user(self, user:str, card_number:str, date, cvv2:int, password):
        if not utils.card_number_check(card_number):
            return(f'{card_number} is invalid card number')
        
        self.cursor.execute(f"select number from card_bank where user_id ='{user}' and number={card_number};")
        user_cards = self.cursor.fetchone()
        if user_cards:
            return(f'{card_number} is already added')
        else:
            print(f"INSERT INTO card_bank(user_id, number, cvv, date, password) VALUES ('{user}', {card_number}, {cvv2}, {date}, {password});")
            self.cursor.execute(f"INSERT INTO card_bank(user_id, number, cvv, date, password) VALUES ('{user}', {card_number}, {cvv2}, {date}, {password});")
            self.connection.commit()
            return(f'{card_number} is added successfully')

    def deposite_withdraw_wallet(self, user_id:str, card_number, cvv2, password, pay_type, amount):
        user_card = self.cursor.execute(f"SELECT * FROM card_bank WHERE user_id = '{user_id}' AND number = {card_number} AND cvv = {cvv2} AND password = {password}")
        user_card = self.cursor.fetchone()

        if user_card:
            if pay_type == 0:
                if self.wallet_balance(user_id) - amount < 0:
                    return False
                else:
                    amount = -amount
            
            
            payment_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pay_hash = utils.payment_code_hash()
            with open('log.transaction', 'a') as f:
                f.write(f"transiction in wallet, user_id='{user_id}',amount={amount},pay_date={payment_time}\n")

            self.cursor.execute(f"UPDATE wallet SET balance = balance + {amount} WHERE user_id = '{user_id}';")
            self.cursor.execute(f"INSERT INTO wallet_transaction(amount, payment_code, card_id, date, pay_type, user_id) VALUES ({amount}, {pay_hash}, {card_number}, '{payment_time}', {pay_type}, '{user_id}');")
            self.connection.commit()
            return True
        else:
            return False
 
    def wallet_balance(self, user:str):
        balance = self.cursor.execute(f"SELECT balance from wallet WHERE user_id='{user}'")
        balance = self.cursor.fetchone()[0]
        self.connection.commit()
        return balance

    def initial_plan_mode(self, user:int):
        self.cursor.execute(f"SELECT * FROM plan WHERE user_id='{user}';")
        if self.cursor.fetchone():
            return('You already have a basic plan')
        else:
            self.cursor.execute(f"INSERT INTO plan(user_id, plan_id, start_time, finish_time) VALUES ('{user}', {1}, '{datetime.now()}', '{datetime.now() + timedelta(days=31)}');")
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
# accounting = Accounting(connection=DB_obj.connection, cursor=DB_obj.cursor)
# accounting.add_card_by_user(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765')
# accounting.initial_setup_wallet(user=user.user['id'])
# accounting.charge_wallet(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765', amount='110')
# accounting.charge_wallet(user=user.user['id'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765', amount='120000')
# print(accounting.wallet_balance(user=user.user['id']))
# buying plan by user
# accounting.initial_plan_mode(user=user.user['id'])
# accounting.buy_plan(user=user.user['id'], plan_name='silver')

class User:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.isAuthenticated = False
        self.user = None

    def register_user(self, username:str, password:str, email:str, birthdate:str, mobile_number:str=None, is_admin:int=0):

        self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_username = self.cursor.fetchone()

        if existing_username:
            return(f"Error: Username '{username}' is already taken. Please choose a different username.")
            

        self.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_email = self.cursor.fetchone()

        if existing_email:
            return(f"Error: Email '{email}' is already used. Please choose a different email.")

        if not utils.validating_email(email):
            return(f"Error: Email '{email}' is not a valid email. Please use a different email.")
            

        if not utils.validating_username(username):
            return("Error: Username should contain both uppercase and lowercase word . Please use a different username.")
            

        if not utils.validating_password(password):
            return("Error: Password should be mpre than 8 character and contain uppercase, lowercase, number and spercial signs . Please use a different password.")
            

        if not utils.validating_mobile_number(mobile_number):
            return (f"Error: Mobile Mumber '{mobile_number}' is not a valid email. Please use a different mobile number.")


        insert_query = """
            INSERT INTO users (username, password, email, mobile_number, birthdate, register_date, last_login_date, last_login_time, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            is_admin
        )

        self.cursor.execute(insert_query, user_data)
        self.connection.commit()
        self.initial_accounting(username=username)
        
        return(f'username {username} is registered successfully, you can login')
        

    def initial_accounting(self, username):
        """
            a func to setup initial wallet and plan to a new user
        """
        self.cursor.execute(f"SELECT uuid FROM users WHERE username = '{username}'")
        user_id = self.cursor.fetchone()[0]
        accounting = Accounting(DB_obj.connection, DB_obj.cursor)
        accounting.initial_setup_wallet(user = user_id)
        accounting.initial_plan_mode(user = user_id)
        
    def login_user(self, username, password):
        if self.isAuthenticated:
            return('You already logged in please logout first')
            

        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, utils.hash_password(password)))
        user_obj = self.cursor.fetchone()

        if not user_obj:
            return('Authentication failed. password or email may be wrong')
            

        columns = [column[0] for column in self.cursor.description]
        self.user = dict(zip(columns, user_obj))

        self.isAuthenticated = True

        self.cursor.execute(f"UPDATE users SET last_login_time = '{datetime.now().time()}' WHERE uuid = '{self.user['uuid']}'")
        self.connection.commit()
        return(f"Dear {self.user['username']} you have just logged in")
        

    def change_profile(self, username=None, email=None, mobile_number=None):
        if not self.isAuthenticated:
            return("Error: User should be logged in first.")

        if username:
            self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            existing_username = self.cursor.fetchone()

            if existing_username:
                return(f"Error: Username '{username}' is already taken. Please choose a different username.")
            else:
                if utils.validating_username(username):
                    self.cursor.execute(f"UPDATE users SET username = '{username}' WHERE uuid = '{self.user['uuid']}'")
                    self.connection.commit()
                    return(f"Dear {self.user['username']} you have just change your username")
                else:
                    return("Error: Username should contain both uppercase and lowercase word . Please use a different username.")

        if email:
            self.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_email = self.cursor.fetchone()

            if existing_email:
                return(f"Error: Email '{email}' is already taken. Please choose a different email.")
            else:
                if utils.validating_email(email):
                    self.cursor.execute(f"UPDATE users SET email = '{email}' WHERE uuid = '{self.user['uuid']}'")
                    self.connection.commit()
                    return(f"Dear {self.user['username']} you have just change your email")
                else:
                    return(f"Error: Email '{email}' is not a valid email. Please use a different email.")

        if mobile_number:
            if utils.validating_mobile_number(mobile_number):
                self.cursor.execute(f"UPDATE users SET mobile_number = '{mobile_number}' WHERE uuid = '{self.user['uuid']}'")
                self.connection.commit()
                return(f"Dear {self.user['username']} you have just change your mobile number")
            else:
                return(f"Error: Mobile Mumber '{mobile_number}' is not a valid number. Please use a different mobile number.")


    def change_password(self, old_password, new_password, new_password_confirm):
        if not self.isAuthenticated:
            return("Error: User should be logged in first.")

        if new_password != new_password_confirm:
            return("Error: new_password and new_password_confirm should be the same.")

        if not utils.validating_password(new_password):
            return("Error: Password should be mpre than 8 character and contain uppercase, lowercase, number and spercial signs . Please use a different password.")
            
        self.cursor.execute("SELECT uuid FROM users WHERE username = %s AND password = %s", (self.user['username'], utils.hash_password(old_password)))
        user_uuid = self.cursor.fetchone()

        if not user_uuid:
            return('Error: username or old password is incorrect. please check and fill again.')
            
        self.cursor.execute(f"UPDATE users SET password = '{utils.hash_password(new_password)}' WHERE uuid = '{self.user['uuid']}'")
        self.connection.commit()

        return(f"Dear {self.user['username']} you have just change your password")

    def logout(self):
        self.isAuthenticated = False
        self.user = None
        return("you log out successfully")
    
    def charge_wallet(self, card_number:str, amount:int):
        if not self.isAuthenticated:
            return("Error: User should be logged in first.")
        self.cursor.execute(f"SELECT * FROM card_bank WHERE number = '{card_number}'")
        card_user_detail = self.cursor.fetchone()
        
        if card_user_detail is None:
            return("the card is not added to your wallet")
        
        elif card_user_detail[2] != self.user["uuid"]:
            return("The entrance card number is not for you")
        
        elif card_user_detail[2] == self.user["uuid"]:
            transaction = Accounting(DB_obj.connection, DB_obj.cursor)
            answer = transaction.deposite_withdraw_wallet(self.user["uuid"], card_user_detail[3], card_user_detail[4], card_user_detail[6], 1, amount)
            if answer:
                return("you wallet charged succesfully")
            else:
                return("somthing went wrong!")
    def __str__(self):

        if not self.isAuthenticated:
            return('You are not logged in')
        print(self.user['username'])


# user = User(DB_obj.connection, DB_obj.cursor)
# user.register_user('Yashar23', 'Thisis@p@ssword1', 'Yashar1989112@gmail.com', '1368-05-23', '09213840549')
# user.login_user('ali', 'Thisis@p@ssword1')
# user.change_password('Thisis@p@ssword1', 'Thisis@p@ssword2', 'Thisis@p@ssword2')
# user.login_user('Yashar23', 'Thisis@p@ssword1')

# user.change_profile(username='Alireza2', email='fuck@thefucking.world')
# accounting = Accounting(connection=DB_obj.connection, cursor=DB_obj.cursor)

# accounting.add_card_by_user(user=user.user['uuid'], card_number='6362141809960843', cvv2='123', date='20201201', password='8765')
# accounting.deposite_withdraw_wallet(user_id=user.user['uuid'], card_number='6362141809960843', cvv2='123', password='8765', amount='110000', pay_type=1)


class Movie:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add_movie(self, user:User, name:str, year:int, age_range:int):
        if not user.isAuthenticated:
            return("login first")
        if(user.user["is_admin"] == 0):
            return("shoma dastresi nadarid")
        
        self.name = name
        self.year = year
        self.age_range = age_range

        self.cursor.execute("SELECT id FROM movie WHERE name = %s", (self.name,))
        existing_movie = self.cursor.fetchone()

        if existing_movie:
            return(f"Error: Movie '{Movie}' is already added.")
        

        insert_query = """
            INSERT INTO movie (name, year, age_range) VALUES (%s, %s, %s)
        """
        movie_data = (name, year, age_range)
        self.cursor.execute(insert_query, movie_data)
        self.connection.commit()
        return(f"Movie '{name}' added") 


    def list_of_movie(self, user:User):
        if not user.isAuthenticated:
            return("login first")
        if(user.user["is_admin"] == 0):
            return("shoma dastresi nadarid")
        
        self.cursor.execute("SELECT id, name FROM movie")
        result = self.cursor.fetchall()
        text = ""
        columns = [column[0] for column in self.cursor.description]
        for row in result:
            temp = dict(zip(columns, row))
            text += (f"id: {temp['id']} ---> name:{temp['name']} \n")
        return(text)

        

# movie = Movie(DB_obj.connection, DB_obj.cursor)
# movie.add_movie('inception', 2016, 18)
# movie.add_movie('The Shawshank Redemption', 1994, 18)

class Screen:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    
    def show_screening(self, user):
        if not user.isAuthenticated :
            return("Error: User should be logged in first.")
        
        self.cursor.execute(f"SELECT * FROM screening WHERE start_time > NOW();")
        result = self.cursor.fetchall()
        text = ""
        columns = [column[0] for column in self.cursor.description]
        for row in result:
            screening = dict(zip(columns, row))
            self.cursor.execute(f"SELECT name FROM movie WHERE uuid = '{screening['movie_id']}'")
            result = self.cursor.fetchone()

            text += (f"{screening['id']} ---> name:{result[0]} -- price:{screening['price']} -- start:{screening['start_time']} -- duration:{screening['end_time']-screening['start_time']}\n")
        return(text)
    def set_movie_screening(self, user:User, movie_id:int, start_time, end_time, price):
        if not user.isAuthenticated:
            return("Error: User should be logged in first.")
        if (user.user["is_admin"] == 0):
            return("shoma dastresi nadarid")

        self.cursor.execute(f"SELECT name FROM movie WHERE id = '{movie_id}'")
        movie_exist = self.cursor.fetchone()

        
        if not movie_exist:
            print('Error : Movie has not declared')
            return

        insert_query = """
            INSERT INTO screening (movie_id, start_time, end_time, price) VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(f"SELECT uuid from movie WHERE id = {movie_id}")
        movie_uuid = self.cursor.fetchone()[0]
        screening_data = (
            movie_uuid,
            start_time,
            end_time,
            price
        )

        self.cursor.execute(insert_query, screening_data)
        self.connection.commit()
        return(f'{movie_exist[0]} added to screen start time : {start_time}')

#screen = Screen(DB_obj.connection, DB_obj.cursor)
# screen.show_screening(user.user)
# screen.set_movie_screening('08d6c4e1-ca42-11ee-a7a0-0242ac113f02', '2024-10-10 20:00:00', '2024-02-06 21:30:00', 100)


class Ticket:
    '''
        This is a ticket class
    '''
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def buy_ticket(self, user:User, screen_id, chair_number:int):
        '''
            buying a ticket
        '''
        if not user.isAuthenticated:
            return("Error: User should be logged in first.")
        
        self.cursor.execute(f"SELECT uuid from screening WHERE id = {screen_id}")
        screen_uuid = self.cursor.fetchone()[0]
        
        self.cursor.execute(f"SELECT uuid FROM ticket WHERE chair_number = {chair_number} AND screen_id = '{screen_uuid}'")
        is_chair_alreay_booked = self.cursor.fetchone()

        if is_chair_alreay_booked:
            return('Error: this chair is already booked plases reserve another')

        if chair_number > 50 or chair_number < 1:
            return("Error : Chair number is out of range")

        self.cursor.execute(f"""SELECT uuid, age_range
                               FROM movie
                               WHERE uuid = (SELECT movie_id
                                           FROM screening 
                                           WHERE id = {screen_id});""")
        movie_data= self.cursor.fetchone()
        self.cursor.execute(f"SELECT price FROM screening WHERE id = {screen_id} AND start_time > NOW();")
        screen_price = self.cursor.fetchone()[0]
        
        if not screen_price:
            return('Error : Screen start time has passed.')

        if not movie_data:
            return('Error : Movie has not found.')

        age = datetime.now().date().year - user.user['birthdate'].year 

        if (movie_data[1] > age):
            return("Error : This movie is not suit for you.")
    
        self.cursor.execute(f"SELECT number, cvv, password FROM card_bank where user_id = '{user.user['uuid']}'")
        card_data = self.cursor.fetchone()

        if not card_data:
            return(f'Error : User has no bank card')

        if datetime.now().date().month == user.user['birthdate'].month and datetime.now().date().day == user.user['birthdate'].day:
            screen_price = screen_price / 2

        transition = Accounting(connection=self.connection, cursor=self.cursor)
        if transition.deposite_withdraw_wallet(user.user['uuid'], card_data[0], card_data[1], card_data[2], 0, screen_price):
            self.cursor.execute(f"INSERT INTO ticket (user_id ,screen_id ,chair_number) VALUES ('{user.user['uuid']}', '{screen_uuid}', {chair_number})")
            self.connection.commit()
            self.cursor.execute(f"""SELECT id
                                    FROM ticket
                                    WHERE user_id = '{user.user['uuid']}' AND
                                    screen_id= '{screen_uuid}' AND
                                    chair_number = {chair_number}
                                    ORDER BY id DESC
                                    LIMIT 1 """)
            ticket_id = self.cursor.fetchone()[0]
            return(f"""you bought a ticket with for {user.user['username']} in chair number {chair_number}. your ticket id is {ticket_id}""")

        else:
            return('Error : card have not found or low cash')


    def show_available_chairs(self, screen_id):
        
        self.cursor.execute(f"SELECT uuid from screening WHERE id = {screen_id}")
        screen_uuid = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT chair_number FROM ticket WHERE screen_id = '{screen_uuid}'")
        empty_chairs = self.cursor.fetchall()

        if not empty_chairs:
            return(f'All the chairs are availbe from number 1 to 50')
        
        booked_chairs = set(num[0] for num in empty_chairs)
        free_chairs = [num for num in range(1, 51) if num not in booked_chairs]
        return(f'list of free chairs in {screen_id} screen : {free_chairs}')
    
    def cancel_ticket(self, user:User, ticket_id):
        if not user.isAuthenticated:
            return("Error: User should be logged in first.")
        

        self.cursor.execute(f"SELECT user_id, screen_id, chair_number FROM ticket WHERE id = '{ticket_id}'")
        ticket_data = self.cursor.fetchone()

        if not ticket_data:
            return('Error : Ticket with this id have not found')

        if (ticket_data[0] != user.user['uuid'] ):
            return("you can't cancel this ticket")

        self.cursor.execute(f"SELECT price, start_time FROM screening WHERE uuid = '{ticket_data[1]}' AND start_time > NOW()")
        screen_data = self.cursor.fetchone()

        if not screen_data:
            return('Error : This screen has already started')

        
        self.cursor.execute(f"SELECT number, cvv, password FROM card_bank where user_id = '{ticket_data[0]}'")
        card_data = self.cursor.fetchone()

        if not card_data:
            return(f'Error : User has no bank card')

        price = screen_data[0] if screen_data[1] - datetime.now() > timedelta(hours=1) else screen_data[0] / 100 * 82
        accounting = Accounting(DB_obj.connection, DB_obj.cursor)
        if accounting.deposite_withdraw_wallet(ticket_data[0], card_data[0], card_data[1], card_data[2], 1, price):
            self.cursor.execute(f"DELETE FROM ticket WHERE id = '{ticket_id}'")
            self.connection.commit()
            return(f'Ticket with has canceled and money returend to your card with {card_data[0]}')
        else:
            return('card is invalid')

#ticket = Ticket(DB_obj.connection, DB_obj.cursor)
# ticket.buy_ticket(user, "e39db067-ca44-11ee-a7a0-0242ac113f02", 40)
# ticket.show_available_chairs(9)
# ticket.cancel_ticket(2)


class Movie_Rate:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def rate_movie(self, user:User, movie_id, rating):
        if not user.isAuthenticated:
            return ("please first login")
        # Validate the rating
        if not (1 <= rating <= 5):
            return("Error: Rate should be between 1 and 5")

        self.cursor.execute(f"SELECT uuid FROM movie WHERE id = '{movie_id}'")
        movie_uuid = self.cursor.fetchone()[0]

        if not movie_uuid:
            return(f"Error: Movie with id {movie_id} does not exist.")

        self.cursor.execute(f"SELECT id FROM `rank` WHERE user_id = '{user.user['uuid']}' AND movie_id = '{movie_uuid}'")
        existing_rank = self.cursor.fetchone()

        if existing_rank:
            return("Error: You have already rated this movie.")

        self.cursor.execute(f"INSERT INTO `rank` (rating, movie_id, user_id)VALUES ({rating}, '{movie_uuid}', '{user.user['uuid']}')")
        self.connection.commit()
        return(f"Rating added: {rating} star for movie {movie_id} by User {user.user['id']}")

    def calculate_average_rating(self, movie_id):
        
        self.cursor.execute(f"SELECT uuid FROM movie WHERE id = '{movie_id}'")
        movie_uuid = self.cursor.fetchone()[0]

        if not movie_uuid:
            return(f"Error: Movie with id {movie_id} does not exist.")

        # Calculate the average rating for the movie
        self.cursor.execute(f"SELECT AVG(rating) FROM `rank` WHERE movie_id = '{movie_uuid}'")
        average_rating = self.cursor.fetchone()[0]
        return str(average_rating)

    def top_rated_movies(self, num_movies):
        # Retrieve the top-rated movies based on average ratings
        top_rated_query = """
            SELECT m.id, m.name, AVG(r.rating) as average_rating
            FROM movie m
            JOIN `rank` r ON m.uuid = r.movie_id
            GROUP BY m.id
            ORDER BY average_rating DESC
            LIMIT %s
        """
        self.cursor.execute(top_rated_query, (num_movies,))
        result = self.cursor.fetchall()
        text = ""
        columns = [column[0] for column in self.cursor.description]
        for row in result:
            temp = dict(zip(columns, row))
            result = self.cursor.fetchone()

            text += (f"id: {temp['id']} ---> name:{temp['name']} -- rate:{temp['average_rating']} \n")
        return(text)

    def get_movie_screenings(self, movie_id):
        # Retrieve the number of screenings for a specific movie
        self.cursor.execute(f"SELECT uuid FROM movie WHERE id = '{movie_id}'")
        movie_uuid = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT COUNT(*) as num_screenings FROM screening WHERE movie_id = '{movie_uuid}'")
        num_movie_screenings = self.cursor.fetchone()[0]
        return str(num_movie_screenings)

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