import pygame
import typing
import yaml

from buttons import Button

OBJECTS = []

def get_screen_size():
    with open('../data/settings.yaml') as settings_file:
        settings = yaml.safe_load(settings_file)
        return [int(settings['screen_size'][0]), int(settings['screen_size'][1])]

def func():
    print("Button Pressed")

def main(*argc, **argv):
    pygame.init()

    mainWin = pygame.display.set_mode((get_screen_size()[0], get_screen_size()[1]))

    # print(str(mainWin))

    OBJECTS.append(Button(mainWin, 30, 30, 200, 50, 'Войти', func))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        for object in OBJECTS:
            object.process()

        pygame.display.flip()

if __name__ == '__main__':
    main()


