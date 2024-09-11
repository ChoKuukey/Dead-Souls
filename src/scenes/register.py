import pygame
import sys

from scenes.scene import Scene

 
from widgets.button import Button
from widgets.label import Label
from widgets.textInput import TextInput


pygame.init()

fpsClock = pygame.time.Clock()

class Register_Scene(Scene):
    def __init__(self, screen, settings: dict, db, db_settings: dict) -> None:
        super().__init__(screen, settings)
        self.__DB = db
        self.__DB_SETTINGS = db_settings
        self.objects = []

    def __str__(self) -> None:
        return "class Register_Scene"

    def __back(self):
        self.run = False

    def main(self) -> None:
        """ Главная функция """
        self.run = True
        self.objects.append(Label(self.screen, (self.screen.get_width() / 2 - 160), 30, 320, 50, 50, 'Регистрация', textColor = (209, 24, 86)))
        self.objects.append(Label(self.screen, (self.screen.get_width() / 2 - 160), 100, 320, 50, 50, 'Почта', textColor = (209, 24, 86)))
        self.objects.append(TextInput(self.screen, (self.screen.get_width() / 2 - 160), 150, 320, 50, None, 40, (255, 255, 255), (165, 102, 219)))
        self.objects.append(Label(self.screen, (self.screen.get_width() / 2 - 160), 220, 320, 50, 50, 'Имя', textColor = (209, 24, 86)))
        self.objects.append(TextInput(self.screen, (self.screen.get_width() / 2 - 160), 270, 320, 50, None, 40, (255, 255, 255), (165, 102, 219)))
        self.objects.append(Label(self.screen, (self.screen.get_width() / 2 - 160), 340, 320, 50, 50, 'Пароль', textColor = (209, 24, 86)))
        self.objects.append(TextInput(self.screen, (self.screen.get_width() / 2 - 160), 390, 320, 50, None, 40, (255, 255, 255), (165, 102, 219)))
        self.objects.append(Button(self.screen, (self.screen.get_width() / 2 - 230), 460, 460, 50, 'Зарегистрироваться', 40, (255, 255, 255), color = (165, 102, 219)))
        self.objects.append(Button(self.screen, (self.screen.get_width() / 2 - 100), 530, 200, 50, 'Назад', 40, (255, 255, 255), self.__back, color = (165, 102, 219)))

        while self.run:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.run = False
            
            for object in self.objects:
                    object.process(event)
                

            pygame.display.flip()
            fpsClock.tick(self.settings['fps'])