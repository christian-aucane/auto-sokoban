from pathlib import Path
import sys
import pygame
from pygame import mixer



from constants import WHITE, WIDTH, HEIGHT
from display.game import GameScreen
from display.menu import MenuScreen
from display.create import CreateScreen
from display.player_screen import PlayerScreen
from game.player import PlayerManager


class SokobanApp:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.player_manager = PlayerManager("players.json")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Sokoban")
        self.running = True

        self.current_screen = MenuScreen(self, self.screen)
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
            self.current_screen = MenuScreen(self, self.screen)
        elif screen_name == "game":
            self.current_screen = GameScreen(self, self.screen)
        elif screen_name == "create":
            self.current_screen = CreateScreen(self, self.screen)
        elif screen_name == "player":
            self.current_screen = PlayerScreen(self, self.screen)
        self.current_screen.load()


    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    grid_path = Path(__file__).resolve().parent / "grid" / "grid.txt"
    app = SokobanApp()
    app.run()
