import pygame
from ui.game import MazeGame
from ui.title_screen import title_screen

if __name__ == "__main__":
    choice = title_screen()  # Gọi menu
    if choice == "start":
        pygame.display.quit()
        pygame.display.init()
        game = MazeGame()
        game.run()