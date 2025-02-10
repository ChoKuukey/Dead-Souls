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

    def __init__(self, screen, settings: dict, client, db, db_config: dict, bg: str | tuple = None, user: str = "example_user") -> None:
        super().__init__(screen, settings, client)
        self.__DB = db
        self.__DB_CONFIG = db_config
        self.objects = []

        self.bg = None
        self.scaledimage = None

        self.user = user

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

        self.disk_count_widget = ImageLabel(self.screen, 1550, 185, 120, 40, 0, "", (255, 255, 255), 0, 'center', "../src/imgs/disk_count.png")
        self.disk_count_label = Label(self.screen, 1512, 188, 120, 40, 25, "0", (255, 255, 255), 255, 'right')
        self.disk_count_label.set_text(f"{self.client.get_user_cd_disk_count(self.user)}")

        self.floppy_disk_count_widget = ImageLabel(self.screen, 1350, 185, 120, 40, 0, "", (0, 0, 0), 0, 'center', "../src/imgs/floppy_disk_count.png")
        self.floppy_disk_count_label = Label(self.screen, 1312, 188, 120, 40, 25, "0", (255, 255, 255), 255, 'right')
        self.floppy_disk_count_label.set_text(f"{self.client.get_user_floppy_disk_count(self.user)}")

        if len(self.user) > 15:
            self.user_name_widget = ImageLabel(self.screen, 100, 1000, 660, 80, 0, "", (231, 106, 58), 255, 'center', "../src/imgs/user_name_label_20.png")
            self.user_name_label = Label(self.screen, 110, 1000, 660, 80, 45, f"{self.user}", (231, 106, 58), 255, 'left')
        else:
            self.user_name_widget = ImageLabel(self.screen, 100, 1000, 500, 80, 0, "", (231, 106, 58), 255, 'center', "../src/imgs/user_name_label_15.png")
            self.user_name_label = Label(self.screen, 110, 1000, 660, 80, 45, f"{self.user}", (231, 106, 58), 255, 'left')

        self.menu_button = ImageButton(self.screen, 1840, 1013, 51, 51, "" , 0, (255, 255, 255), lambda: self.__exit_game(), False, (255, 255, 255), "../src/imgs/menu_button.png")

        self.objects.append(self.disk_count_widget)
        self.objects.append(self.disk_count_label)

        self.objects.append(self.floppy_disk_count_widget)
        self.objects.append(self.floppy_disk_count_label)

        self.objects.append(self.user_name_widget)
        self.objects.append(self.user_name_label)

        self.objects.append(self.menu_button)

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