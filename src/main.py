""" Главный модуль запуска """

import pygame
import os
import sys

from scenes.MainMenuScene import MainScene

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.dataFuncs import (
    get_settings, 
    get_db_config
)

pygame.init()

__SETTINGS = get_settings("../data/settings.yaml")
__DB_CONFIG = get_db_config("../data/db/db_config.yaml")
__DB = None

__SCREEN = pygame.display.set_mode(((__SETTINGS['screen_size'][0]), __SETTINGS['screen_size'][1]))
pygame.display.set_caption('Dead Souls')


if __name__ == '__main__':
    mainWin = MainScene(__SCREEN, __SETTINGS, __DB, __DB_CONFIG, bg="../src/imgs/cool_bg.png")
    mainWin.main()
