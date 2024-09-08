import pygame
import typing
import yaml


class MainWindow:
    def __init__(self, screen_size: typing.Tuple, *argc, **argv) -> None: 
        screen = pygame.display.set_mode((screen_size[0], screen_size[1]))

    def __str__(self):
        with open("data/settings.yaml", 'r') as settings:
            read_data = yaml.load(settings, Loader = yaml.FullLoader)
        return f"Dead Souls - {read_data['version']}"