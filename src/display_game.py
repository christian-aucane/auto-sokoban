from pathlib import Path
import sys

import pygame

from constants import Sizes, Colors, Paths

from display.game import GameScreen
from display.menu import MenuScreen
from display.create import CreateScreen
from utils.sound_manager import SoundManager


class SokobanApp:
    def __init__(self):
        pygame.init()

        self.sound_manager = SoundManager()
        self.sound_manager.load_music("menu", Paths.MUSIC / "menu.mp3")
        self.sound_manager.load_music("game", Paths.MUSIC / "game.mp3")
        self.sound_manager.load_music("create", Paths.MUSIC / "create.mp3")

        self.screen = pygame.display.set_mode((Sizes.WIDTH, Sizes.HEIGHT))
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

            self.screen.fill(Colors.WHITE)
            self.current_screen.update()
            pygame.display.flip()
            self.clock.tick(60)  # 60FPS
            
    def switch_screen(self, screen_name):
        self.current_screen.quit()
        if screen_name == "menu":
            pygame.time.delay(600)
            self.current_screen = MenuScreen(self, self.screen)
        elif screen_name == "game":
            self.current_screen = GameScreen(self, self.screen)
        elif screen_name == "create":
            self.current_screen = CreateScreen(self, self.screen)
        self.current_screen.load()

    def quit(self):
        self.sound_manager.stop_music()
        self.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    grid_path = Paths.LEVELS / "Original grid.txt"
    app = SokobanApp()
    app.run()
