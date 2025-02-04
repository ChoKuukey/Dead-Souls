""" Модуль главного игрового экрана """
import pygame
import sys
import time

from scenes.scene import Scene
# from client.client import Client

from widgets.button import (
    ImageButton
)

from widgets.label import ImageLabel
from widgets.label import Label


pygame.init()

fpsClock = pygame.time.Clock()

class MainGameScene(Scene):
    """ Модуль главного игрового экрана """

    def __init__(self, screen, settings: dict, client, db, db_config: dict, bg: str | tuple = None) -> None:
        super().__init__(screen, settings, client)
        self.__DB = db
        self.__DB_CONFIG = db_config
        self.objects = []

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

    def __exit_game(self) -> None:
        self.run = False
        sys.exit()

    def main(self) -> None:

        self.run = True

        self.money_count_widget = ImageLabel(self.screen, 1550, 185, 120, 40, 0, "", (0, 0, 0), 0, 'center', "../src/imgs/money_count.png")
        self.money_count_label = Label(self.screen, 1510, 188, 120, 40, 33, "0", (255, 255, 255), 255, 'right')

        self.objects.append(self.money_count_widget)
        self.objects.append(self.money_count_label)
        # self.objects.append(ImageButton(self.screen, 30, 330, 325, 110, 'Выход', 50, (255, 255, 255), lambda: self.__exit_game(), imagePath = "../src/imgs/btn.png"))
        
        print(">> Запуск Основной игровой сцены")

        while self.run:
            if isinstance(self.scaledimage, pygame.surface.Surface):
                self.screen.blit(self.scaledimage, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                self.event = self.event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.run = False
            
            for object in self.objects:
                object.process(self.event)

            pygame.display.flip()
            fpsClock.tick(self.settings['fps'])