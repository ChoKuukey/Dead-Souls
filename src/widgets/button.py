""" Модуль с кнопками """

import pygame

from widgets.widget import Widget


class Button(Widget):
    """ Абстрактная Кнопка """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, buttonText: str = 'Button', 
                fontSize: int = 20, fontColor: tuple = (255, 255, 255), function = None, onePress = False, color: tuple = (0, 0, 0), hoverColor: tuple = (255, 255, 255)) -> None:
        super().__init__(window, x, y, width, height)

        self.font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)
        self.fontColor = fontColor

        self.window = window
        self.buttonText = buttonText
        self.function = function
        self.color = color
        self.hoverColor = hoverColor
        self.onePress = onePress
        self.alreadyPressed = False

        self.buttonSurf = self.font.render(self.buttonText, True,self.fontColor)


    def process(self, event) -> None:
        mousePos = pygame.mouse.get_pos()   # get mouse position

        self.surface.fill(self.color)

        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                if self.onePress:
                    self.function()
                elif not self.alreadyPressed:
                    self.function()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.surface.blit(self.buttonSurf, [
            self.rect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.rect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])

        self.draw()

        
class ImageButton(Button):
    """ Класс для кнопки с картинкой """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, buttonText: str = 'Button', 
                fontSize: int = 20, fontColor: tuple = (255, 255, 255), function = None, onePress = False, hoverColor: tuple = (255, 255, 255), imagePath: str = None) -> None:
        super().__init__(window, x, y, width, height, buttonText, fontSize, fontColor, function, onePress, hoverColor)

        self.image = pygame.image.load(imagePath).convert_alpha()
        self.scaledimage = pygame.transform.scale(self.image, (width, height)) 

    def process(self, event) -> None:
        mousePos = pygame.mouse.get_pos()   # get mouse position

        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                if self.onePress:
                    self.function()
                elif not self.alreadyPressed:
                    self.function()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.surface.blit(self.scaledimage, (0, 0))

        self.surface.blit(self.buttonSurf, [
            self.rect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.rect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])

        self.draw()
