from db.db import (
    Connection,
)

from scenes.register import Register_Scene


class Authorization():
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.db = None
        self.cursor = None

    def __str__(self) -> str:
        return "class Authorization"

    def signin(self) -> None:
        print("Sign IN")

    def signup(self, screen, settings: dict) -> None:
        self.connection.connect()
        self.db = self.connection.db
        self.cursor = self.connection.cursor

        register_scene = Register_Scene(screen, settings, self.db, self.connection.settings)
        register_scene.main()


        self.connection.close(self.db, self.cursor)