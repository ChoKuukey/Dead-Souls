""" Модуль Виджета """
from abc import ABC, abstractmethod
import pygame

pygame.init()

class Widget(ABC):
    """ Абстрактный виджет """
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))

    def draw(self) -> None:
        self.window.blit(self.surface, self.rect)

    @abstractmethod
    def process(self, event) -> None:
        pass