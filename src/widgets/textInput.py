from widgets.widget import Widget
import pygame
import time


pygame.init()

class TextInput(Widget):
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, placeholder: str = None, fontSize: int = 20, 
                 textColor: tuple = (255, 255, 255), bg_color = (0, 0, 0), passt: bool = False, length: int = 20) -> None:
        super().__init__(window, x, y, width, height)

        try:
            self.font = pygame.font.Font('../fonts/OffBit-101Bold.ttf', fontSize)
        except:
            print(">> TextInput ошиб: Файл шрифта не найден")
        self.fontSize = fontSize

        self.placeholder = None
        self.isPlH = False  # Есть ли плейсхолдер

        if self.placeholder is not None:
            self.isPlH = True

        self.textColor = textColor
        self.bg_color = bg_color

        # Флаг пароля
        self.passt = passt

        # Текст, который будет показываться
        if self.placeholder is not None:
            self.text = self.placeholder
        else:
            self.text = ""

        # длина текста
        self.length = length

        # Переменная текста
        self.textvariable = ""

        self.active = False   # Флаг активности

        self.TeInSurface = self.font.render(self.text, True, self.textColor)

    def process(self, event) -> None:
        self.surface.fill(self.bg_color)
        if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
            # Если пользователь нажал на инпут бокс
            if self.rect.collidepoint(event.pos):
                if not self.active:
                    # Если активен, то выключаем
                    self.active = True
            else:
                self.active = False
        if event is not None and event.type == pygame.KEYDOWN and self.active:
            
            if event.key == pygame.K_RETURN:
                time.sleep(0.125)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                time.sleep(0.125)
                self.text = self.text[:-1]
                self.textvariable = self.textvariable[:-1]
        if event is not None and event.type == pygame.TEXTINPUT and self.active and len(self.textvariable) < self.length:
            # Флаг пароля
            if self.passt:
                self.textvariable += event.text
                self.text += "*"
            else:
                self.text += event.text
                self.textvariable += event.text
            time.sleep(0.125)

        self.TeInSurface = self.font.render(self.text, True, self.textColor)

        self.surface.blit(self.TeInSurface, [
            self.rect.width / 20,
            self.rect.height / 2 - self.TeInSurface.get_rect().height / 2
        ])

        self.draw()


class ImageTextInput(TextInput):
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, placeholder: str = None, fontSize: int = 20, 
                 textColor: tuple = (255, 255, 255), imagePath: str = None, passt: bool = False, length: int = None) -> 20:
        super().__init__(window, x, y, width, height, placeholder, fontSize, textColor, None, passt, length)

        # Изображение и его приведение к нужному размеру
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.scaledimage = pygame.transform.scale(self.image, (width, height))

    def process(self, event) -> None:
        if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
            # Если пользователь нажал на инпут бокс
            if self.rect.collidepoint(event.pos):
                if not self.active:
                    # Если активен, то выключаем
                    self.active = True
            else:
                self.active = False
        if event is not None and event.type == pygame.KEYDOWN and self.active:  
            if event.key == pygame.K_BACKSPACE:
                time.sleep(0.125)
                self.text = self.text[:-1]
                self.textvariable = self.textvariable[:-1]
        if event is not None and event.type == pygame.TEXTINPUT and self.active and len(self.textvariable) < self.length:
            # Флаг пароля
            if self.passt:
                self.textvariable += event.text
                self.text += "*"
            else:
                self.text += event.text
                self.textvariable += event.text
            time.sleep(0.125)

        # Рисуем изображение
        self.surface.blit(self.scaledimage, (0, 0))
        # Текст
        self.TeInSurface = self.font.render(self.text, True, self.textColor)

        self.surface.blit(self.TeInSurface, [
            self.rect.width / 20,
            self.rect.height / 2 - self.TeInSurface.get_rect().height / 2
        ])

        self.draw()