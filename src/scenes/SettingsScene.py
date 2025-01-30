from scenes.scene import Scene
import pygame
import sys

from widgets.button import (
    ImageButton
)

pygame.init()

fpsClock = pygame.time.Clock()

class SettingsScene(Scene):
    """ Сцена настроек """
    def __init__(self, screen, settings: dict, client, bg: str | tuple = None) -> None:
        super().__init__(screen, settings, client)

        self.bg = None
        self.scaledimage = None

        self.objects = []

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

    def __back(self):
        self.run = False

    def main(self):
        print(">> Запуск Сцены Настроек")
        self.run = True

        self.objects.append(ImageButton(self.screen, (self.screen.get_width() / 2 - 200), 810, 190, 70, 'Назад', 45, (255, 255, 255), self.__back, imagePath="../src/imgs/btn.png"))

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