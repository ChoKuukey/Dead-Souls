""" Главный модуль запуска """

import pygame
import os
import sys
import time
import threading
from multiprocessing import Process

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

scene_params = [__SCREEN, __SETTINGS, __DB, __DB_CONFIG]

if __name__ == '__main__':
    client = Client()
    client.scene_params = scene_params

    client_thread = threading.Thread(target=client.connect_to_server, args=("89.189.179.132", 8623))
    client_thread.daemon = True
    client_thread.start()

    # client_process = Process(target=client.connect_to_server, args=("89.189.179.132", 8623), name="Dead-Souls-Client", daemon=True)
    # client_process.start()

    mainWin = MainScene(__SCREEN, __SETTINGS, client, __DB, __DB_CONFIG, bg="../src/imgs/cool_bg.png")
    client.main_menu_scene = mainWin
    mainWin.main()
    # ccs = ConfirmCode_scene(__SCREEN, __SETTINGS, client, __DB, __DB_CONFIG, bg="../src/imgs/cool_bg.png", sent_code=None, email="example@gmail.com")
    # ccs.main()
    # time.sleep(3)
    # maim_game_scene = MainGameScene(__SCREEN, __SETTINGS, client, __DB, __DB_CONFIG, "../src/imgs/main_game_scene.png", "JazzMaster")
    # maim_game_scene.main()