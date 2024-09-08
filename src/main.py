import pygame
from main_window import MainWindow


def main(*argc, **argv):
    pygame.init()

    mainWin = MainWindow((500, 750))

    print(str(mainWin))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.display.flip()

if __name__ == '__main__':
    main()