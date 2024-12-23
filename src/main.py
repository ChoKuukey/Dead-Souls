""" Главный модуль запуска """

import pygame
import os
import sys
from multiprocessing import Process
import threading

from scenes.MainMenuScene import MainScene
from scenes.ConfirmCodeScene import ConfirmCode_scene
from scenes.MainGameScrene import MainGameScene

from client.client import Client

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from data.dataFuncs import (
    get_settings, 
    get_db_config
)

pygame.init()

game_icon = pygame.image.load("../src/imgs/icon.png")
pygame.display.set_icon(game_icon)

__SETTINGS = get_settings("../data/settings.yaml")
__DB_CONFIG = get_db_config("../data/db/db_config.yaml")
__DB = None

__SCREEN = pygame.display.set_mode(((__SETTINGS['screen_size'][0]), __SETTINGS['screen_size'][1]))
pygame.display.set_caption('Dead Souls')


if __name__ == '__main__':
    client = Client()


    client_thread = threading.Thread(target=client.connect_to_server, args=("127.0.0.1", 8080))
    client_thread.daemon = True
    client_thread.start()

    mainWin = MainScene(__SCREEN, __SETTINGS, client, __DB, __DB_CONFIG, bg="../src/imgs/cool_bg.png")
    mainWin.main()
    # ccs = ConfirmCode_scene(__SCREEN, __SETTINGS, __DB, __DB_CONFIG, bg="../src/imgs/cool_bg.png")
    # ccs.main()
    # maim_game_scene = MainGameScene(__SCREEN, __SETTINGS, __DB, __DB_CONFIG, "../src/imgs/main_bg.png")
    # maim_game_scene.main()