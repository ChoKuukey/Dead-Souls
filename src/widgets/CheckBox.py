from widgets.widget import Widget
import pygame
import typing


pygame.init()


class CheckBox(Widget):
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, function: typing.Callable) -> None:
        super().__init__(window, x, y, width, height)

        self.function = function

        self.is_active = True

        self.alreadyPressed = False

        self.on_image = pygame.image.load("../src/imgs/basic_check_box_on.png").convert_alpha()
        self.on_image_scaled = pygame.transform.scale(self.on_image, (width, height))

        self.off_image = pygame.image.load("../src/imgs/basic_check_box_off.png").convert_alpha()
        self.off_image_scaled = pygame.transform.scale(self.off_image, (width, height))

    def process(self, event) -> None:

        if self.is_active:
            self.surface.blit(self.on_image_scaled, (0, 0))
        else:
            self.surface.blit(self.off_image_scaled, (0, 0))

        mousePos = pygame.mouse.get_pos()   # get mouse position

        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                if not self.alreadyPressed:
                    self.function()
                    if self.is_active:
                        self.is_active = False
                        self.surface.blit(self.off_image_scaled, (0, 0))
                        print(">> Чекбок снят")
                    else:
                        self.is_active = True
                        self.surface.blit(self.on_image_scaled, (0, 0))
                        print(">> Чекбок поднят")

                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.surface.blit(self.surface, [
            self.rect.width / 2 - self.surface.get_rect().width / 2,
            self.rect.height / 2 - self.surface.get_rect().height / 2
        ])

        self.draw()