""" Модуль с лэйблами """
import pygame
from widgets.widget import Widget


pygame.init()

class Label(Widget):
    """ Лэйбл """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, fontSize: int, text: str, textColor: tuple = (255, 255, 255), bg_alpha: int = 255, anchor: str = 'center') -> None:
        super().__init__(window, x, y, width, height)

        self.__font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)

        self.__textColor = textColor
        self.anchor = anchor

        self.text = text
        self.surface.set_alpha(bg_alpha)
        self.labelSurface = self.__font.render(self.text, True, self.__textColor)
        self.labelSurface.set_alpha(bg_alpha)

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def set_text(self, text: str) -> None:
        self.text = text
        self.labelSurface = self.__font.render(self.text, True, self.__textColor)

    def process(self, event) -> None:
        self.surface.fill((0, 0, 0, 0))
        if self.anchor == 'center':
            self.surface.blit(self.labelSurface, [
                self.rect.width / 2 - self.labelSurface.get_rect().width / 2,
                self.rect.height / 2 - self.labelSurface.get_rect().height / 2
            ])
        elif self.anchor == 'left':
            self.surface.blit(self.labelSurface, [
                0,
                self.rect.height / 2 - self.labelSurface.get_rect().height / 2
            ])
        elif self.anchor == 'right':
            self.surface.blit(self.labelSurface, [
                self.rect.width - self.labelSurface.get_rect().width,
                self.rect.height / 2 - self.labelSurface.get_rect().height / 2
            ])
        self.draw()


class ImageLabel(Label):
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, fontSize: int, text: str, textColor: tuple = (255, 255, 255), bg_alpha: int = 255, anchor: str = 'center', bg: str = None) -> None:
        super().__init__(window, x, y, width, height, fontSize, text, textColor, bg_alpha, anchor)

        self.image = pygame.image.load(bg).convert_alpha()
        self.scaledimage = pygame.transform.scale(self.image, (width, height)) 

    def process(self, event) -> None:

        self.surface.blit(self.scaledimage, (0, 0))
        
        if self.anchor == 'center':
            self.surface.blit(self.labelSurface, [
                self.rect.width / 2 - self.labelSurface.get_rect().width / 2,
                self.rect.height / 2 - self.labelSurface.get_rect().height / 2
            ])
        elif self.anchor == 'left':
            self.surface.blit(self.labelSurface, [
                0,
                self.rect.height / 2 - self.labelSurface.get_rect().height / 2
            ])
        elif self.anchor == 'right':
            self.surface.blit(self.labelSurface, [
                self.rect.width - self.labelSurface.get_rect().width,
                self.rect.height / 2 - self.labelSurface.get_rect().height / 2
            ])
        self.draw()