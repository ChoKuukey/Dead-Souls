from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, screen, settings: dict) -> None:
        self.screen = screen
        self.settings = settings
        self.run = False

    @abstractmethod
    def main(self, *argc) -> None:
        pass