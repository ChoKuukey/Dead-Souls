""" Модуль для регистрации """
import psycopg2
import datetime
import re
import pygame


from widgets.label import Label


from db.db import (
    Connection
)
 
from scenes.ConfirmCodeScene import ConfirmCode_scene

pygame.init()


class Registration:
    """ класс для регистрации """
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.db = None
        self.cursor = None

        """
        + - один или более символов из предыдущего набора
        \. - точка
        {2,} - два или более символов из предыдущего набора
        $ - конец строки
        (?=exp) - Проверка на совпадение с выражением exp продолжения строки
        . - любой символ
        * - ноль или более символов из предыдущего набора
        \d - цифра
        """
        self.__email_re_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        self.__password_re_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

    def __str__(self) -> str:
        return "class Registration"

    def register(self, confirm_code_screen, main_game_screen, settings: dict, db_config: dict, email: str, username: str, password: str, error_label: Label) -> None:
        self.connection.connect()
        self.db = self.connection.db
        self.cursor = self.connection.cursor

        """ Проверка на уникальность почты и правильность почты """
        try:
            self.cursor.execute(f"SELECT * FROM {db_config['table']} WHERE email = %s", (email,))
            if self.cursor.fetchone() is not None:
                error_label.set_text("Такая почта уже зарегистрирована")
                self.connection.close(self.db, self.cursor) 
                return
            elif not re.match(self.__email_re_pattern, email):
                error_label.set_text("Некорректная почта")
                self.connection.close(self.db, self.cursor) 
                return
        except psycopg2.OperationalError:
            error_label.set_text(">> Не удалось подключиться к базе данных")
            self.connection.close(self.db, self.cursor) 
            return
        
        """ Проверка на уникальность имени и правильность имени """
        try:
            self.cursor.execute(f"SELECT * FROM {db_config['table']} WHERE name = %s", (username,))
            if self.cursor.fetchone() is not None:
                error_label.set_text("Такое имя уже зарегистрировано")
                self.connection.close(self.db, self.cursor) 
                return
            elif len(username) < 3:
                error_label.set_text("Имя должно быть больше трех символов")
                self.connection.close(self.db, self.cursor) 
                return
        except psycopg2.OperationalError:
            error_label.set_text(">> Не удалось подключиться к базе данных")
            self.connection.close(self.db, self.cursor) 
            return
        
        """ Проверка пароля """
        try:
            if len(password) < 8:
                error_label.set_text("Пароль должен быть больше 8 символов")
                self.connection.close(self.db, self.cursor) 
                return
        except psycopg2.OperationalError:
            error_label.set_text(">> Не удалось подключиться к базе данных")
            self.connection.close(self.db, self.cursor) 
            return

        """ Если пользователей нет, то id должен начинаться с 0 """
        id = self.cursor.execute(f"SELECT MAX(id) FROM {db_config['table']}")
        max_id = self.cursor.fetchone()
        if max_id[0] is None:
            max_id = 0
        else:
            max_id = max_id[0]
        max_id += 1


        # Дата создания
        time_r = datetime.datetime.now()
        create_at = time_r.strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.cursor.execute(f"INSERT INTO {db_config['table']} (id, email, name, password_digest, create_at) VALUES (%s, %s, %s, %s, %s)", (max_id, email, username, password, create_at))
            self.db.commit()
        except psycopg2.OperationalError:
            print(">> Не удалось зарегистрироваться")
            return

        self.connection.close(self.db, self.cursor) 
