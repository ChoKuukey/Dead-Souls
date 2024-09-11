""" Главный модуль запуска """

import pygame
import typing
import sys
import yaml

from scenes.scene import Scene

from widgets.button import Button

from db.db import (
    Connection
)
from db.authorization import (
    Authorization
)


pygame.init()

__SETTINGS = {}
__DB_CONFIG = {}

#
##########################################
# Полуение настроек
with open('../data/settings.yaml') as settings_file:
    __SETTINGS = yaml.load(settings_file, Loader=yaml.FullLoader)

""" Открытие файла db_config.yaml """
try:
    with open("../src/db/db_config.yaml") as settings_file:
        __DB_CONFIG = yaml.load(settings_file, Loader=yaml.FullLoader)
except FileNotFoundError:
    print(">> Не удалось открыть файл db_config.yaml")
#
###########################################
#



__SCREEN = pygame.display.set_mode(((__SETTINGS['screen_size'][0]), __SETTINGS['screen_size'][1]))
pygame.display.set_caption('Dead Souls')


__DB = None

fpsClock = pygame.time.Clock()

#
############################################
#

class MainScene(Scene):
    def __init__(self, screen, settings: dict, db, db_config: dict) -> None:
        super().__init__(screen, settings)
        self.__DB = db
        self.__DB_CONFIG = db_config
        self.objects = []
        self.connetion = Connection(self.__DB, self.__DB_CONFIG)
        self.authorization = Authorization(self.connetion)

    def __str__(self) -> str:
        return "class MainScene"

    def main(self, *argc) -> None:
        """ Главная функция """

        self.run = True
        self.objects.append(Button(self.screen, 30, 30, 200, 50, 'Войти', 40, (200, 200, 200), self.authorization.signin, color = (165, 102, 219)))
        self.objects.append(Button(self.screen, 30, 130, 200, 50, 'Зарег', 40, (200, 200, 200), lambda: self.authorization.signup(self.screen, self.settings), color = (165, 102, 219)))
        self.objects.append(Button(self.screen, 30, 230, 200, 50, 'Выход', 40, (200, 200, 200), lambda: sys.exit(0), color = (165, 102, 219)))

        while self.run:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.run = False
            
            for object in self.objects:
                object.process(event)

            pygame.display.flip()
            fpsClock.tick(self.settings['fps'])



if __name__ == '__main__':
    mainWin = MainScene(__SCREEN, __SETTINGS, __DB, __DB_CONFIG)
    mainWin.main()
#
############################################
#