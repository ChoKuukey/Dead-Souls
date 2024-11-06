""" Модуль главного меню """
import typing
import sys
import pygame

from scenes.scene import Scene
from scenes.register import Register_Scene
from scenes.singin import SignInScene

from widgets.button import (
    Button,
    ImageButton
)

# from db.db import (
#     Connection
# )
# from db.authorization import (
#     Authorization
# )

from client.client import Client

pygame.init()

fpsClock = pygame.time.Clock()

class MainScene(Scene):
    def __init__(self, screen, settings: dict, client, db, db_config: dict, bg: str | tuple = None) -> None:
        super().__init__(screen, settings, client)
        self.__DB = db
        self.__DB_CONFIG = db_config

        self.bg = None
        self.scaledimage = None

        if isinstance(bg, str):
            try:
                self.bg = pygame.image.load(bg).convert_alpha()
                self.scaledimage = pygame.transform.scale(self.bg, (settings['screen_size'][0], settings['screen_size'][1])) 
            except FileNotFoundError:
                print(">> Не удалось загрузить фоновое изображение")
            else: 
                self.bg = (0, 0, 0)
        elif isinstance(bg, tuple):
            self.bg = bg
        else:
            print(">> Фон может быть только изображением или цветом в формате (0, 0, 0)!")
            self.bg = (0, 0, 0)

        self.objects = []
        # self.connection = Connection(self.__DB, self.__DB_CONFIG)

        # self.connection.connect()

        # self.db = self.connection.db
        # self.cursor = self.connection.cursor

        # self.connection.init_db()

        # self.connection.close(self.db, self.cursor)

        # self.authorization = Authorization(self.connection)

    def __str__(self) -> str:
        return "class MainScene"
    
    def __exit_game(self) -> None:
        self.client.close_connection_to_server()
        self.run = False
        sys.exit()

    def __run_registration_scene(self):
        register_scene = Register_Scene(self.screen, self.settings, self.client, self.__DB, self.__DB_CONFIG, bg="../src/imgs/cool_bg.png")
        register_scene.main()

    def __run_autorization_scene(self):
        autorization_scene = SignInScene(self.screen, self.settings, self.client, self.__DB, self.__DB_CONFIG, bg="../src/imgs/cool_bg.png")
        autorization_scene.main()

    def main(self) -> None:
        """ Главная функция """

        print(">> Запуск Dead Souls")

        self.run = True
        self.objects.append(ImageButton(self.screen, 30, 30, 325, 110, 'Войти', 50, (255, 255, 255), lambda: self.__run_autorization_scene(), imagePath = "../src/imgs/btn.png"))
        self.objects.append(ImageButton(self.screen, 30, 180, 325, 110, 'Регистрация', 50, (255, 255, 255), lambda: self.__run_registration_scene(), imagePath = "../src/imgs/btn.png"))
        self.objects.append(ImageButton(self.screen, 30, 330, 325, 110, 'Выход', 50, (255, 255, 255), lambda: self.__exit_game(), imagePath = "../src/imgs/btn.png"))

        print(">> Приложение запущено...")

        

        while self.run:
            if isinstance(self.scaledimage, pygame.surface.Surface):
                self.screen.blit(self.scaledimage, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                self.event = event
                if event.type == pygame.QUIT:
                    self.client.close_connection_to_server()
                    pygame.quit()
                    sys.exit()
                    self.run = False
            
            for object in self.objects:
                object.process(self.event)

            pygame.display.flip()
            fpsClock.tick(self.settings['fps'])