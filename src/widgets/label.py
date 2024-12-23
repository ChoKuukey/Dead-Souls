""" Модуль с лэйблами """
import pygame
from widgets.widget import Widget


pygame.init()

class Label(Widget):
    """ Лэйбл """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, fontSize: int, text: str, textColor: tuple = (255, 255, 255), bg_alpha: int = 255) -> None:
        super().__init__(window, x, y, width, height)

        self.__font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)

        self.__textColor = textColor

        self.text = text
        self.surface.set_alpha(bg_alpha)
        self.__labelSurface = self.__font.render(self.text, True, self.__textColor)
        self.__labelSurface.set_alpha(255)

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def set_text(self, text: str) -> None:
        self.text = text
        self.__labelSurface = self.__font.render(self.text, True, self.__textColor)

    def process(self, event) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.__labelSurface, [
            self.rect.width / 2 - self.__labelSurface.get_rect().width / 2,
            self.rect.height / 2 - self.__labelSurface.get_rect().height / 2
        ])
        self.draw()