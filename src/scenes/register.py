import pygame
import sys

from scenes.scene import Scene

from scenes.ConfirmCodeScene import ConfirmCode_scene
from scenes.MainGameScreen import MainGame_scene
 
from widgets.button import (
    Button,
    ImageButton
    )
from widgets.label import Label
from widgets.textInput import (
    TextInput,
    ImageTextInput
)

from db.db import Connection

from db.registration import Registration

pygame.init()

fpsClock = pygame.time.Clock()

class Register_Scene(Scene):
    def __init__(self, screen, settings: dict, db, db_config: dict, bg: str | tuple = None) -> None:
        super().__init__(screen, settings)
        self.__DB = db
        self.__DB_CONFIG = db_config

        self.objects = []
        self.connetion = Connection(self.__DB, self.__DB_CONFIG)
        self.registration = Registration(self.connetion)

        self.bg = None
        self.scaledimage = None

        if isinstance(bg, str):
            try:
                self.bg = pygame.image.load(bg).convert_alpha()
                self.scaledimage = pygame.transform.scale(self.bg, (settings['screen_size'][0], settings['screen_size'][1])) 
            except FileNotFoundError:
                print(">> Не удалось загрузить фоновое изображение")
            else: 
                self.bg = (0, 0, 0)
        elif isinstance(bg, tuple):
            self.bg = bg
        else:
            print(">> Фон может быть только изображением или цветом в формате (0, 0, 0)!")
            self.bg = (0, 0, 0)

    def __str__(self) -> None:
        return "class Register_Scene"

    def __back(self):
        self.run = False

    def main(self) -> None:
        print(">> Запуск Запуск сцены регистрации")
        """ Главная функция """
        email_input = ImageTextInput(self.screen, (self.screen.get_width() / 2 - 200), 130, 400, 80, "Почта", 25, (255, 255, 255), imagePath="../src/imgs/textinput.png", length = 19)
        user_name_input = ImageTextInput(self.screen, (self.screen.get_width() / 2 - 200), 250, 400, 80, "Имя", 35, (255, 255, 255), imagePath="../src/imgs/textinput.png", length = 20)
        passwrod_input = ImageTextInput(self.screen, (self.screen.get_width() / 2 - 200), 370, 400, 80, "Пароль", 45, (255, 255, 255), imagePath="../src/imgs/textinput.png", passt = True, length = 35)
        error_label = Label(self.screen, 0, 460, self.screen.get_width(), 50, 40, '', textColor = (178,34,34), bg_alpha = 0)
        # confirm_code_input = ImageTextInput(self.screen, (self.screen.get_width() / 2 + 10), 610, 190, 70, "Код", 35, (255, 255, 255), imagePath="../src/imgs/textinput.png", length = 7)
        
        self.run = True

        self.objects.append(Label(self.screen, (self.screen.get_width() / 2 - 160), 20, 320, 50, 50, 'Регистрация', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(Label(self.screen, 295, 90, 100, 50, 30, 'Почта', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(email_input)
        self.objects.append(Label(self.screen, 280, 210, 100, 50, 30, 'Имя', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(user_name_input)
        self.objects.append(Label(self.screen, 305, 330, 100, 50, 30, 'Пароль', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(passwrod_input)
        self.objects.append(error_label)
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() / 2 - 200), 510, 400, 80, 'Подтвердить', 50, (255, 255, 255), 
                                        function = lambda: self.registration.register(self.screen, 
                                                                                      MainGame_scene, 
                                                                                      self.settings,
                                                                                      self.__DB_CONFIG, 
                                                                                      email_input.textvariable, 
                                                                                      user_name_input.textvariable, 
                                                                                      passwrod_input.textvariable, 
                                                                                      error_label), 
                                        imagePath="../src/imgs/btn.png"))
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() / 2 - 200), 610, 190, 70, 'Назад', 45, (255, 255, 255), self.__back, imagePath="../src/imgs/btn.png"))
        # self.objects.append(confirm_code_input)

        while self.run:
            if isinstance(self.scaledimage, pygame.surface.Surface):
                self.screen.blit(self.scaledimage, (0, 0))
            else:
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