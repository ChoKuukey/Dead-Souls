""" Модуль подтверждения кода """
import pygame
import sys


from scenes.scene import Scene

from scenes.MainGameScrene import MainGameScene

from widgets.button import (
    ImageButton
)

from widgets.label import Label

from widgets.textInput import (
    ImageTextInput
)

from db.db import (
    Connection
)

pygame.init()

fpsClock = pygame.time.Clock()


class ConfirmCode_scene(Scene):
    """ Модуль подтверждения кода """

    def __init__(self, screen, settings: dict, db, db_config: dict, bg: str | tuple = None, sent_code: str = None, email: str = None) -> None:
        super().__init__(screen, settings)
        self.__DB = db
        self.__DB_CONFIG = db_config
        self.__SENT_CODE = sent_code
        self.__EMAIL = email # почта пользователя, которую нужно активировать
        self.objects = []
    
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

    def confrim_registration(self, code: str, send_code: str, error_label: Label) -> None:
        if code != send_code:
            print(">> Код не подтвержден")
            error_label.set_text("Неправильный код")
            return
        else:
            print(">> Код подтвержден")
            """ обновление is_active у учетки """
            connection = Connection(self.__DB, self.__DB_CONFIG)
            connection.connect()
            self.__DB = connection.db
            cursor = connection.cursor
            cursor.execute(f"UPDATE {self.__DB_CONFIG['table']} SET is_active = TRUE WHERE email = %s", (self.__EMAIL,))
            self.__DB.commit()
            connection.close(self.__DB, cursor)
            print(">> Учетка активирована")
            error_label.set_text("")

            self.run = False

            self.maim_game_scene = MainGameScene(self.screen, self.settings, self.__DB, self.__DB_CONFIG, "../src/imgs/main_bg.png")
            self.maim_game_scene.main()


    def main(self) -> None:
        print(">> Запуск Сцены подтверждения кода")
        self.run = True

        label = Label(self.screen, (self.screen.get_width() / 2 - 400), (self.screen.get_height() / 2 - 150), 800, 50, 40, "Введите код потверждения с почты", (255, 255, 255))

        code_enter = ImageTextInput(self.screen, (self.screen.get_width() / 2 - 150), (self.screen.get_height() / 2 - 35), 
                                    300, 75, None, 40, (255, 255, 255), imagePath="../src/imgs/textinput.png", length = 6)
        
        error_label = Label(self.screen, 0, (self.screen.get_height() / 2 + 40), self.screen.get_width(), 50, 40, "", (178,34,34))

        accept_button = ImageButton(self.screen, (self.screen.get_width() / 2 - 150), (self.screen.get_height() / 2 + 80), 300, 50, "Подтвердить", 20, (255, 255, 255), 
                                    lambda: self.confrim_registration(code_enter.text, self.__SENT_CODE, error_label), True, imagePath="../src/imgs/btn.png")

        self.objects.append(label)
        self.objects.append(code_enter)
        self.objects.append(error_label)
        self.objects.append(accept_button)

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