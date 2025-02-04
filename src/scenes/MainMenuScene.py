""" Модуль главного меню """
import typing
import sys
import pygame

from scenes.scene import Scene
from scenes.register import Register_Scene
from scenes.singin import SignInScene
from scenes.SettingsScene import SettingsScene

from widgets.button import (
    ImageButton
)

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

    def __str__(self) -> str:
        return "class MainScene"
    
    def __exit_game(self) -> None:
        self.client.close_connection_to_server()
        self.run = False
        sys.exit()

    def __run_registration_scene(self):
        register_scene = Register_Scene(self.screen, self.settings, self.client, self.__DB, self.__DB_CONFIG, bg="../src/imgs/cool_bg.png")
        self.client.register_scene = register_scene
        register_scene.main()

    def __run_autorization_scene(self):
        autorization_scene = SignInScene(self.screen, self.settings, self.client, self.__DB, self.__DB_CONFIG, bg="../src/imgs/cool_bg.png")
        self.client.signin_scene = autorization_scene
        autorization_scene.main()

    def __run_settings_scene(self):
        settings_scene = SettingsScene(self.screen, self.settings, self.client, bg="../src/imgs/bg_settings.png")
        self.client.settings_scene = settings_scene
        settings_scene.main()

    def main(self) -> None:
        """ Главная функция """

        print(">> Запуск Dead Souls")

        self.run = True
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() - self.screen.get_width() / 2 + 490), (self.screen.get_height() - self.screen.get_height() / 2 - 200), 
                                        400, 112, 'Войти', 50, (255, 255, 255), lambda: self.__run_autorization_scene(), imagePath = "../src/imgs/btn.png"))
        
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() - self.screen.get_width() / 2 + 490), (self.screen.get_height() - self.screen.get_height() / 2 - 80), 
                                        400, 112, 'Регистрация', 50, (255, 255, 255), lambda: self.__run_registration_scene(), imagePath = "../src/imgs/btn.png"))
        
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() - self.screen.get_width() / 2 + 490), (self.screen.get_height() - self.screen.get_height() / 2 + 40), 
                                        400, 112, 'Настройки', 50, (255, 255, 255), lambda: self.__run_settings_scene(), imagePath = "../src/imgs/btn.png"))
        
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() - self.screen.get_width() / 2 + 490), (self.screen.get_height() - self.screen.get_height() / 2 + 160), 
                                        400, 112, 'Выход', 50, (255, 255, 255), lambda: self.__exit_game(), imagePath = "../src/imgs/btn.png"))

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