""" Модуль с кнопками """

import pygame

from widgets.widget import Widget


class Button(Widget):
    """ Абстрактная Кнопка """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, buttonText: str = 'Button', 
                fontSize: int = 20, fontColor: tuple = (255, 255, 255), function = None, onePress = False, color: tuple = (0, 0, 0)) -> None:
        super().__init__(window, x, y, width, height)

        self.__font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)
        self.__fontColor = fontColor

        self.__window = window
        self.__buttonText = buttonText
        self.__function = function
        self.__color = color
        self.__onePress = onePress
        self.__alreadyPressed = False

        self.__buttonSurf = self.__font.render(self.__buttonText, True,self.__fontColor)


    def process(self, event) -> None:
        mousePos = pygame.mouse.get_pos()   # get mouse position

        self.surface.fill(self.__color)

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

        
     
