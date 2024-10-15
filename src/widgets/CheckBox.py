from widgets.widget import Widget
import pygame
import typing


pygame.init()


class CheckBox(Widget):
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, function: typing.Callable) -> None:
        super().__init__(window, x, y, width, height)

        self.image = pygame.image.load('../src/imgs/check_box_img.png').convert_alpha()
        self.scaledimage = pygame.transform.scale(self.image, (width-5, height-5))

        self.function = function

        self.is_active = True

        self.alreadyPressed = False

    def process(self, event) -> None:
        mousePos = pygame.mouse.get_pos()   # get mouse position

        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                if not self.alreadyPressed:
                    self.function()
                    if self.is_active:
                        self.is_active = False
                        print(">> Чекбок снят")
                    else:
                        self.is_active = True
                        print(">> Чекбок поднят")

                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.surface.blit(self.scaledimage, (5, 5))

        self.surface.blit(self.surface, [
            self.rect.width / 2 - self.surface.get_rect().width / 2,
            self.rect.height / 2 - self.surface.get_rect().height / 2
        ])

        self.draw()