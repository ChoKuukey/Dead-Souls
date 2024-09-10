""" Главный модуль запуска """

import pygame
import typing
import sys
import yaml

from widgets.button import Button

__OBJECTS = []

################################
# Полуение настроек
__SETTINGS = []

with open('../data/settings.yaml') as settings_file:
    __SETTINGS = yaml.load(settings_file, Loader=yaml.FullLoader)
################################

def signin():
    print("Sign IN")

def signup():
    print("Sign UP")

fpsClock = pygame.time.Clock()

def main(*argc, **argv) -> None:
    pygame.init()

    mainWin = pygame.display.set_mode(((__SETTINGS['screen_size'][0]), __SETTINGS['screen_size'][1]))

    __OBJECTS.append(Button(mainWin, 30, 30, 200, 50, 'Войти', signin))
    __OBJECTS.append(Button(mainWin, 30, 130, 200, 50, 'Зарег', signup))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        for object in __OBJECTS:
            object.process()

        pygame.display.flip()
        fpsClock.tick(__SETTINGS['fps'])

if __name__ == '__main__':
    main()


