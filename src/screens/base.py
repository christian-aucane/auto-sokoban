import pygame

from constants import MUSIC_DIR


class BaseScreen:
    def __init__(self, app, screen, music):
        self.app = app
        self.screen = screen
        self.music = self.load_music(music)

    @staticmethod
    def load_music(music):
        return pygame.mixer.Sound(MUSIC_DIR / music)

    def play_music(self):
        self.music.play(-1)

    def stop_music(self):
        self.music.stop()

    def load(self):
        self.play_music()
    
    def quit(self):
        self.stop_music()