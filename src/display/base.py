import pygame

from constants import FONT, Sizes, Colors, Paths


class BaseScreen:
    def __init__(self, app, screen, music_name, sound_effects=None, background_image_file=""):
        self.app = app
        self.screen = screen
        self.music = self.app.music_channels[music_name]
        if not self.app.music_channel.get_busy():
            self.app.music_channel.play(self.music, loops=-1) 
        if sound_effects is None:
            sound_effects = {}
        self.sound_effects = {}
        for i, (name, path) in enumerate(sound_effects.items()):
            channel = pygame.mixer.Channel(i + 1)  
            sound = pygame.mixer.Sound(path)
            sound.set_volume(1)
            self.sound_effects[name] = (channel, sound)
        self.background_image = pygame.transform.scale(
            pygame.image.load(Paths.BACKGROUND_IMAGES / background_image_file),
            (Sizes.WIDTH, Sizes.HEIGHT)
        )
        self.main_buttons = []

    @staticmethod
    def load_music(music):
        return pygame.mixer.Sound(Paths.MUSIC / music)
    

    @staticmethod
    def load_sound_effect(filename):
        return pygame.mixer.Sound(Paths.SOUND_EFFECTS / filename)
    
    def draw_background_image(self):
        self.screen.blit(self.background_image, (0, 0))

    def draw_main(self):
        self.draw_background_image()
        for button in self.main_buttons:
            self.draw_button(button)

    def draw_button(self, button, is_active=False):
        if is_active:
            button.set_text_color(Colors.BUTTON_ACTIVE_TEXT)
        elif button.is_clicked(pygame.mouse.get_pos()):
            button.set_text_color(Colors.BUTTON_HOVER_TEXT)
        else:
            button.set_text_color(Colors.BUTTON_TEXT)
        button.draw()

    def draw_text(self, text, color, **pos):
        text_surface = FONT.render(text, True, color)
        text_rect = text_surface.get_rect(**pos)
        self.screen.blit(text_surface, text_rect)

    def play_music(self):
        self.music.set_volume(0.2)
        self.music.play(-1)

    def stop_music(self):
        self.music_channel.stop()

    def quit(self):
        pass

    def play_sound_effect(self, name):
        channel, sound = self.sound_effects.get(name, (None, None))
        if channel is None or sound is None:
            raise ValueError(f"Sound effect '{name}' not found")
        channel.play(sound)

    def load(self):
        if self.app.current_music != self.music:
            self.app.music_channel.stop()
            self.app.music_channel.play(self.music, loops=-1)
            self.app.current_music = self.music
    
    def update(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def handle_event(self, event):
        raise NotImplementedError("Subclass must implement abstract method")
