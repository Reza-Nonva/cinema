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
        CREATE TABLE IF NOT EXISTS `plan_transaction`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `plan_id` BIGINT NOT NULL,
            `payment_code` BIGINT NOT NULL,
            `date` DATETIME NOT NULL,
            `user_id` INT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS `card_bank`(
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `number` VARCHAR(16) NOT NULL,
            `cvv` BIGINT NOT NULL,
            `date` DATE NOT NULL,
            `password` BIGINT NOT NULL
        );
        
        ALTER TABLE
            `card_bank` ADD UNIQUE `card_bank_number_unique`(`number`);
        CREATE TABLE IF NOT EXISTS `wallet_transaction`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `payment_code` BIGINT NOT NULL,
            `card_id` VARCHAR(16) NOT NULL,
            `date` DATETIME NOT NULL,
            `pay_type` BIGINT NOT NULL,
            `user_id` INT NOT NULL
        );
        ALTER TABLE
            `wallet_transaction` ADD INDEX `wallet_transaction_payment_code_index`(`payment_code`);
        ALTER TABLE
            `users` ADD UNIQUE `users_username_unique`(`username`);
        ALTER TABLE
            `users` ADD UNIQUE `users_email_unique`(`email`);
        CREATE TABLE `wallet`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `balance` BIGINT NOT NULL DEFAULT '0'
        );
        CREATE TABLE IF NOT EXISTS `plan`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL,
            `plan_id` VARCHAR(255) NOT NULL,
            `start_time` DATETIME NOT NULL,
            `finish_time` DATETIME NOT NULL
        );
        ALTER TABLE
            `plan_transaction` ADD CONSTRAINT `plan_transaction_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `wallet`(`user_id`);
        ALTER TABLE
            `wallet` ADD CONSTRAINT `wallet_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `users`(`id`);
        ALTER TABLE
            `wallet_transaction` ADD CONSTRAINT `wallet_transaction_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `wallet`(`user_id`);
        ALTER TABLE
            `card_bank` ADD CONSTRAINT `card_bank_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `users`(`id`);
        ALTER TABLE
            `plan` ADD CONSTRAINT `plan_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `users`(`id`);
        ALTER TABLE
            `wallet_transaction` ADD CONSTRAINT `wallet_transaction_card_id_foreign` FOREIGN KEY(`card_id`) REFERENCES `card_bank`(`number`);
        """

        self.cursor.execute(create_accounting_tables)
        self.connection.commit()


DB_obj = DBconnection('tai.liara.cloud', 33428, 'root', 'ErOmibw13imQzlzw3TIgyE10', 'focused_driscoll')