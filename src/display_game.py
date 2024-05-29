from pathlib import Path
import sys
import pygame
from pygame import mixer


from constants import WIDTH, HEIGHT, WHITE
from screens.menu import MenuScreen
from screens.create import CreateScreen


class SokobanApp:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Sokoban")
        self.running = True

        self.menu = MenuScreen(self, self.screen)
        self.create = CreateScreen(self, self.screen)

        self.current_screen = self.menu
        self.current_screen.load()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.current_screen.handle_event(event)

            self.screen.fill(WHITE)
            self.current_screen.update()
            pygame.display.flip()
            self.clock.tick(60)  # 60FPS

    def switch_screen(self, screen_name):
        self.current_screen.quit()
        if screen_name == "menu":
            self.current_screen = self.menu
        elif screen_name == "game":
            print("GAME")
        elif screen_name == "create":
            self.current_screen = self.create
        self.current_screen.load()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    grid_path = Path(__file__).resolve().parent / "grid" / "grid.txt"
    app = SokobanApp()
    app.run()
