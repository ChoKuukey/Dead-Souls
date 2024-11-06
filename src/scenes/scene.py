from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, screen, settings: dict, client) -> None:
        self.screen = screen
        self.settings = settings
        self.run = False

        self.event = None

        self.client = client

    @abstractmethod
    def main(self, *argc) -> None:
        pass