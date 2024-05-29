import pygame

from constants import MUSIC_DIR, SOUND_EFFECTS_DIR


class BaseScreen:
    def __init__(self, app, screen, music, sound_effects={}):
        self.app = app
        self.screen = screen
        self.music = self.load_music(music)
        self.sound_effects = sound_effects

    @staticmethod
    def load_music(music):
        return pygame.mixer.Sound(MUSIC_DIR / music)

    @staticmethod
    def load_sound_effect(filename):
        return pygame.mixer.Sound(SOUND_EFFECTS_DIR / filename)
    
    def play_music(self):
        self.music.play(-1)

    def stop_music(self):
        self.music.stop()

    def play_sound_effect(self, sound_effect):
        sound_effect = self.sound_effects.get(sound_effect)
        if sound_effect is None:
            raise ValueError(f"Sound effect '{sound_effect}' not found")
        sound_effect.play()

    def load(self):
        self.play_music()
    
    def quit(self):
        self.stop_music()

    def update(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def handle_event(self, event):
        raise NotImplementedError("Subclass must implement abstract method")
    