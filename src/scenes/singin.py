import pygame
import sys
import psycopg2

from scenes.scene import Scene

from scenes.MainGameScrene import MainGameScene
 
from widgets.button import (
    Button,
    ImageButton
    )
from widgets.label import Label
from widgets.textInput import (
    TextInput,
    ImageTextInput
)
from widgets.CheckBox import CheckBox

from db.db import Connection

pygame.init()

fpsClock = pygame.time.Clock()

class SignInScene(Scene):
    def __init__(self, screen, settings: dict, client, db, db_config: dict, bg: str | tuple = None) -> None:
        super().__init__(screen, settings, client)
        self.__DB = db
        self.__DB_CONFIG = db_config

        self.objects = []
        self.connection = Connection(self.__DB, self.__DB_CONFIG)

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
        return "class SignInScene"

    def __back(self):
        self.run = False

    def change_pass_vision(self, password_input: TextInput | ImageTextInput) -> None:
        if password_input.passt:
            password_input.passt = False
            password_input.text = password_input.textvariable
            # password_input.process(None)
        else:
            password_input.passt = True
            password_input.textvariable = password_input.text
            password_input.text = "*" * len(password_input.textvariable)
            # password_input.process(None)

    def account_enter(self, email: str, password: str, error_label: Label) -> None:
        self.connection.connect()
        self.db = self.connection.db
        self.cursor = self.connection.cursor

        user = None

        try:    
            self.cursor.execute(f"SELECT * FROM {self.__DB_CONFIG['table']} WHERE email = %s", (email,))
            user = self.cursor.fetchone()
            if user is None:
                error_label.set_text("Пользователь не найден")
                self.connection.close(self.__DB, self.cursor)
                return
            if user[6] is False:
                error_label.set_text("Пользователь не найден")
                self.connection.close(self.__DB, self.cursor)
                return
        except psycopg2.OperationalError:
            error_label.set_text(">> Не удалось подключиться к базе данных")
            self.connection.close(self.__DB, self.cursor)
            return
        
        try:
            self.cursor.execute(f"SELECT * FROM {self.__DB_CONFIG['table']} WHERE email = %s AND password_digest = %s", (email, password))
            if self.cursor.fetchone() is None:
                error_label.set_text("Неправильный пароль")
                self.connection.close(self.__DB, self.cursor)
                return
        except psycopg2.OperationalError:
            error_label.set_text(">> Не удалось подключиться к базе данных")
            self.connection.close(self.__DB, self.cursor)
            return

        error_label.set_text("Успешно")

        main_game = MainGameScene(self.screen, self.settings, self.client, self.db, self.__DB_CONFIG, bg = "../src/imgs/main_bg.png")
        main_game.main()

        self.connection.close(self.__DB, self.cursor)
            

    def main(self) -> None:
        print(">> Запуск Запуск сцены авторизации")
        """ Главная функция """
        email_input = ImageTextInput(self.screen, (self.screen.get_width() / 2 - 200), 250, 400, 80, "Почта", 25, (255, 255, 255), imagePath="../src/imgs/textinput.png", length = 30)
        passwrod_input = ImageTextInput(self.screen, (self.screen.get_width() / 2 - 200), 370, 400, 80, "Пароль", 45, (255, 255, 255), imagePath="../src/imgs/textinput.png", passt = True, length = 35)
        error_label = Label(self.screen, 0, 460, self.screen.get_width(), 50, 40, "", textColor = (178,34,34), bg_alpha = 0)
        
        self.run = True

        self.objects.append(Label(self.screen, (self.screen.get_width() / 2 - 250), 150, 500, 50, 50, 'Войти в аккаунт', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(Label(self.screen, 295, 210, 100, 50, 30, 'Почта', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(email_input)
        self.objects.append(Label(self.screen, 305, 330, 100, 50, 30, 'Пароль', textColor = (255, 255, 255), bg_alpha = 0))
        self.objects.append(passwrod_input)
        self.objects.append(error_label)
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() / 2 - 200), 510, 400, 80, 'Подтвердить', 50, (255, 255, 255), 
                                        function = lambda: self.client.account_enter(email_input.textvariable, passwrod_input.textvariable, error_label),
                                        imagePath="../src/imgs/btn.png"))
        self.objects.append(CheckBox(self.screen, (self.screen.get_width() / 2 + 200), 380, 50, 50, function = lambda: self.change_pass_vision(passwrod_input)))
        self.objects.append(ImageButton(self.screen, (self.screen.get_width() / 2 - 200), 610, 190, 70, 'Назад', 45, (255, 255, 255), self.__back, imagePath="../src/imgs/btn.png"))

        # self.objects.append(confirm_code_input)

        while self.run:
            if isinstance(self.scaledimage, pygame.surface.Surface):
                self.screen.blit(self.scaledimage, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                self.event = event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.run = False
            
            for object in self.objects:
                object.process(self.event)
                

            pygame.display.flip()
            fpsClock.tick(self.settings['fps'])