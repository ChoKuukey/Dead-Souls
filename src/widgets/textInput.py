from widgets.widget import Widget
import pygame
import time


pygame.init()

class TextInput(Widget):
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, placeholder: str = None, fontSize: int = 20, textColor: tuple = (255, 255, 255), bg_color = (0, 0, 0), *flags) -> None:
        super().__init__(window, x, y, width, height)

        self.__font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)
        self.__fontSize = fontSize

        self.__placeholder = placeholder
        self.__textColor = textColor
        self.__bg_color = bg_color
        self.__text = '123'

        self.__active = False   # Флаг активности

        self.__TeInSurface = self.__font.render(self.__text, True, self.__textColor)

    def process(self, event) -> None:
        self.surface.fill(self.__bg_color)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если пользователь нажал на инпут бокс
            if self.rect.collidepoint(event.pos):
                if not self.__active:
                    # Если активен, то выключаем
                    self.__active = True
                    # pygame.key.start_text_input()
                    print(self.__active)
            else:
                self.__active = False
                # pygame.key.stop_text_input()
        if event.type == pygame.KEYDOWN and self.__active:
            
            if event.key == pygame.K_RETURN:
                time.sleep(0.1)
                print(self.__text)
                self.__text = ''
                self.typing = True
            elif event.key == pygame.K_BACKSPACE:
                time.sleep(0.1)
                self.__text = self.__text[:-1]
                self.typing = True
        elif event.type == pygame.TEXTINPUT and self.__active:
            time.sleep(0.12)
            self.__text += event.text
            self.__typing = True
        self.__TeInSurface = self.__font.render(self.__text, True, self.__textColor)

        self.surface.blit(self.__TeInSurface, [
            5,
            self.rect.height / 2 - self.__TeInSurface.get_rect().height / 2
        ])

        self.draw()
