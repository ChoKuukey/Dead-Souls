""" Модуль главного игрового экрана """
import pygame
import sys

from scenes.scene import Scene


pygame.init()

fpsClock = pygame.time.Clock()

class MainGameScene(Scene):
    """ Модуль главного игрового экрана """

    def __init__(self, screen, settings: dict, db, db_config: dict, bg: str = None) -> None:
        super().__init__(screen, settings)
        self.__DB = db
        self.__DB_CONFIG = db_config
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

    def main(self, *argc) -> None:

        self.run = True

        
        print(">> Запуск Основной игровой сцены")

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