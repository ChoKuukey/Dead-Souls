""" Модуль с лэйблами """
import pygame
from widgets.widget import Widget


pygame.init()

class Label(Widget):
    """ Лэйбл """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, fontSize: int, text: str, textColor: tuple = (255, 255, 255)) -> None:
        super().__init__(window, x, y, width, height)

        self.__font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)

        self.__fontSize = fontSize
        self.__text = text
        self.labelSurface = self.__font.render(self.__text, True, textColor)


    def process(self, event) -> None:
        self.surface.blit(self.labelSurface, [
            self.rect.width / 2 - self.labelSurface.get_rect().width / 2,
            self.rect.height / 2 - self.labelSurface.get_rect().height / 2
        ])
        self.draw()