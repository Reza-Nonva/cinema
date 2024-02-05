import mysql.connector

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
        # self.create_table()

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
        create_movie_table_query = """
        CREATE TABLE IF NOT EXISTS `movie`(
        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL,
        `year` BIGINT NOT NULL,
        `age_range` BIGINT NOT NULL
        );
        """
        create_accounting_tables = """

        CREATE TABLE IF NOT EXISTS `card_bank`(
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `number` VARCHAR(16) NOT NULL UNIQUE,
            `cvv` BIGINT NOT NULL,
            `date` DATE NOT NULL,
            `password` BIGINT NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
        );
        
        
        CREATE TABLE `wallet`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `balance` BIGINT NOT NULL DEFAULT '0',
            FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
        );

        CREATE TABLE IF NOT EXISTS `wallet_transaction`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `payment_code` BIGINT NOT NULL,
            `card_id` VARCHAR(16) NOT NULL,
            `date` DATETIME NOT NULL,
            `pay_type` BIGINT NOT NULL,
            `user_id` INT NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES `wallet`(`user_id`),
            FOREIGN KEY(`card_id`) REFERENCES `card_bank`(`number`)

        );
        CREATE TABLE IF NOT EXISTS `plan_transaction`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `plan_id` BIGINT NOT NULL,
            `payment_code` BIGINT NOT NULL,
            `date` DATETIME NOT NULL,
            `user_id` INT NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES `wallet`(`user_id`)
        );
        CREATE TABLE IF NOT EXISTS `plan`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `plan_id` VARCHAR(255) NOT NULL,
            `start_time` DATETIME NOT NULL,
            `finish_time` DATETIME NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES `users`(`id`);
        );
        """
        create_screen_query = """
        CREATE TABLE `screening`(
        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `movie_id` BIGINT UNSIGNED NOT NULL,
        `start_time` DATETIME NOT NULL,
        `end_time` DATETIME NOT NULL,
        `price` BIGINT NOT NULL,
         FOREIGN KEY(`movie_id`) REFERENCES `movie`(`id`)
        );
        """
        temp = """CREATE TABLE IF NOT EXISTS `plan`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `plan_id` VARCHAR(255) NOT NULL,
            `start_time` DATETIME NOT NULL,
            `finish_time` DATETIME NOT NULL,
            FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
        );"""
        self.cursor.execute(temp)
        self.connection.commit()


DB_obj = DBconnection('tai.liara.cloud', 33428, 'root', 'ErOmibw13imQzlzw3TIgyE10', 'focused_driscoll')

# DB_obj.cursor.execute('ALTER TABLE users MODIFY COLUMN is_user BOOL NOT NULL DEFAULT FALSE;')