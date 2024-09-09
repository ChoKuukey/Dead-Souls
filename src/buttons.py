import pygame
from fonts import button_font



class Button():
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, buttonText: str = 'Button', function = None, onePress = False) -> None:
        self.__window = window
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__buttonText = buttonText
        self.__function = function
        self.__onePress = onePress
        self.__alreadyPressed = False

        self.__buttonSurface = pygame.Surface((self.__width, self.__height))
        self.__buttonRect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        self.__buttonSurf = button_font.render(buttonText, True, (255, 255, 255))


    def process(self) -> None:
        mousePos = pygame.mouse.get_pos()   # get mouse position

        self.__buttonSurface.fill(255)

        if pygame.mouse.get_pressed(num_buttons = 3)[0]:
            if self.__onePress:
                self.__function()
            elif not self.__alreadyPressed:
                self.__function()
                self.__alreadyPressed = True
        else:
            self.__alreadyPressed = False

        self.__buttonSurface.blit(self.__buttonSurf, [
            self.__buttonRect.width / 2 - self.__buttonSurf.get_rect().width / 2,
            self.__buttonRect.height / 2 - self.__buttonSurf.get_rect().height / 2
        ])

        self.__window.blit(self.__buttonSurface, self.__buttonRect)
     
