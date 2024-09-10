""" Модуль с кнопками """

import pygame

from fonts import button_font

from widgets.widget import Widget


class Button(Widget):
    """ Абстрактная Кнопка """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, buttonText: str = 'Button', function = None, onePress = False) -> None:
        super().__init__(window, x, y, width, height)
        self.__window = window
        self.__buttonText = buttonText
        self.__function = function
        self.__onePress = onePress
        self.__alreadyPressed = False

        self.__buttonSurf = button_font.render(buttonText, True, (255, 255, 255))


    def process(self) -> None:
        mousePos = pygame.mouse.get_pos()   # get mouse position

        self.surface.fill(255)

        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                if self.__onePress:
                    self.__function()
                elif not self.__alreadyPressed:
                    self.__function()
                    self.__alreadyPressed = True
            else:
                self.__alreadyPressed = False

        self.surface.blit(self.__buttonSurf, [
            self.rect.width / 2 - self.__buttonSurf.get_rect().width / 2,
            self.rect.height / 2 - self.__buttonSurf.get_rect().height / 2
        ])

        self.draw()

        
     
