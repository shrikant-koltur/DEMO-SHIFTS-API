import os
import mysql.connector
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

# Access environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")
db_port = os.getenv("DB_PORT")

class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        if exception_type:
            self.connection.rollback()  # Rollback transaction if an exception occurs
        else:
            self.connection.commit()  # Commit transaction if no exception occurs
        self.cursor.close()
        self.connection.close()


class MysqlDatabase(Database):
    """MySQL Database context manager"""

    def __init__(self) -> None:
        self.driver = mysql.connector
        super().__init__(self.driver)

    def connect_to_database(self):
        config = {
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'port': db_port,
            'database': db_database,
            'raise_on_warnings': True,
            'autocommit': False  # Disable autocommit to manage transactions manually
        }
        return self.driver.connect(**config)