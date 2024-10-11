""" Основной модуль для работы с базой данных PostgreSQL """

import psycopg2
import yaml


class Connection:
    """ Класс для подключения к базе данных """
    def __init__(self, db, settings: dict) -> None:
        self.db = db
        self.cursor = None
        self.settings: dict = settings
    
    def __str__(self) -> str:
        return "class Connection"

    def init_db(self):
        """ Метод для создания базы данных """
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS  {self.settings['table']} (id SERIAL PRIMARY KEY, email VARCHAR(255), name VARCHAR(255), password VARCHAR(255))")
            self.db.commit()
        except psycopg2.OperationalError:
            print(">> Не удалось создать базу данных")

    def connect(self) -> psycopg2.connect:
        """ Метод для подключения к бд """
        try:
            self.db = psycopg2.connect(dbname = self.settings['dbname'], user =  self.settings['user'], host = self.settings['host'], password = self.settings['password'])
        except psycopg2.OperationalError:
            print(">> Не удалось подключиться к базе данных")
        else:
            print(">> Подключение к базе данных прошло успешно") 
            self.cursor = self.db.cursor() 

    def close(self, db: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor) -> None:
        """ Метод для закрытия подлючения с бд """
        if db is not None and cursor is not None:
            try:
                cursor.close()
                db.close()
                print(">> Подключение к базе данных закрыто")
            except psycopg2.Error:
                print(">> Не удалось закрыть подключение к базе данных")
        else:
            print(">> Невозможно закрыть подключение к базе данных, т.к. соединение не существует")
