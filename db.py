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

DB_obj = DBconnection('tai.liara.cloud', 33428, 'root', 'ErOmibw13imQzlzw3TIgyE10', 'focused_driscoll')
