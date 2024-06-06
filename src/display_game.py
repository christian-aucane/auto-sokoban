from pathlib import Path
import sys

import pygame

from constants import Sizes, Colors, Paths

from display.game import GameScreen
from display.menu import MenuScreen
from display.create import CreateScreen


class SokobanApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(15)

        self.current_music = None
        self.music_channels = {
            "game": pygame.mixer.Sound(Paths.MUSIC / "game.mp3"),
            "create": pygame.mixer.Sound(Paths.MUSIC / "create.mp3"),
            "menu": pygame.mixer.Sound(Paths.MUSIC / "menu.mp3"),
        }
        for channel in self.music_channels.values():
            channel.set_volume(0.4)
        self.music_channel = pygame.mixer.Channel(0)

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
        self.music_channel.stop()  # Arrêtez la musique lorsque vous passez au menu
        if screen_name == "menu":
            self.current_screen = MenuScreen(self, self.screen)
            self.music_channel.play(self.music_channels["menu"], loops=-1)
        elif screen_name == "game":
            self.current_screen = GameScreen(self, self.screen)
            if not self.music_channel.get_busy():
                self.music_channel.play(self.music_channels["game"], loops=-1)
        elif screen_name == "create":
            self.current_screen = CreateScreen(self, self.screen)
            if not self.music_channel.get_busy():
                self.music_channel.play(self.music_channels["create"], loops=-1)
        self.current_screen.load()

    def quit(self):
        self.current_screen.stop_music() 
        self.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    grid_path = Paths.LEVELS / "Original grid.txt"
    app = SokobanApp()
    app.run()
