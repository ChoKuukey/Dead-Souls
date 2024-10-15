""" Модуль для авторизации """

from db.db import (
    Connection,
)

from scenes.register import Register_Scene
from scenes.singin import SignInScene


class Authorization():
    """ Класс для авторизации """
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.db = None
        self.cursor = None

    def __str__(self) -> str:
        return "class Authorization"

    def signin(self, screen, settings: dict) -> None:
        self.connection.connect()
        self.db = self.connection.db
        self.cursor = self.connection.cursor

        register_scene = SignInScene(screen, settings, self.db, self.connection.settings, bg="../src/imgs/cool_bg.png")
        register_scene.main()


        self.connection.close(self.db, self.cursor)

    def signup(self, screen, settings: dict) -> None:
        self.connection.connect()
        self.db = self.connection.db
        self.cursor = self.connection.cursor

        register_scene = Register_Scene(screen, settings, self.db, self.connection.settings, bg="../src/imgs/cool_bg.png")
        register_scene.main()


        self.connection.close(self.db, self.cursor)
