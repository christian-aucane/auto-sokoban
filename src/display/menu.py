import pygame

from .base import BaseScreen
from utils.widgets import ImageButton, Slider
from constants import MAIN_MENU_SLIDERS_X, Colors, Sizes, Paths, MAIN_MENU_BUTTONS_X


class MenuScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(
            "menu",
            app=app,
            screen=screen,
            background_image_path= Paths.BACKGROUND_IMAGES / "menu.png",
        )
        self.main_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=100,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Play",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="play"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=200,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Settings",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="settings"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=300,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Create",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="create"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=400,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Quit",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit"
            )
        ]
        self.current_screen = "main"

        self.sound_manager.load_sound_effect("click", Paths.SOUND_EFFECTS / "click.mp3")
        self.sound_manager.load_sound_effect("click_main", Paths.SOUND_EFFECTS / "click_main_menu.mp3")
        self.sound_manager.load_sound_effect("save", Paths.SOUND_EFFECTS / "save_grid.mp3")

        self.initial_settings_values = {
            "music_volume": self.sound_manager.music_volume,
            "sound_effect_volume": self.sound_manager.sound_effect_volume
        }
        self.settings_sliders = [
            Slider(
                screen=screen,
                x=MAIN_MENU_SLIDERS_X,
                y=100,
                width=Sizes.MAIN_MENU_SLIDER_WIDTH,
                height=Sizes.MAIN_MENU_SLIDER_HEIGHT,
                min_value=0,
                max_value=100,
                initial_value=int(self.sound_manager.music_volume * 100),
                bg_color=Colors.SLIDER_BG,
                slider_color=Colors.SLIDER,
                knob_color=Colors.SLIDER_KNOB,
                label="Music Volume",
                data="music_volume",
            ),
            Slider(
                screen=screen,
                x=MAIN_MENU_SLIDERS_X,
                y=200,
                width=Sizes.MAIN_MENU_SLIDER_WIDTH,
                height=Sizes.MAIN_MENU_SLIDER_HEIGHT,
                min_value=0,
                max_value=100,
                initial_value=int(self.sound_manager.sound_effect_volume * 100),
                bg_color=Colors.SLIDER_BG,
                slider_color=Colors.SLIDER,
                knob_color=Colors.SLIDER_KNOB,
                label="Sound Effects Volume",
                data="sound_effect_volume",
            )
        ]
        self.settings_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=300,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Save",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="save",
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=400,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Quit",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit",
            ),
        ]

    def draw_settings(self):
        for button in self.settings_buttons:
            button.draw()
        for slider in self.settings_sliders:
            slider.draw()

    def load_settings(self):
        self.current_screen = "settings"

    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "settings":
            self.draw_settings()

    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        self.sound_manager.play_sound_effect("click")
                        if button.data == "play":
                            self.app.switch_screen("game")
                        elif button.data == "settings":
                            self.load_settings()
                        elif button.data == "create":
                            self.app.switch_screen("create")
                        elif button.data == "quit":
                            pygame.time.delay(800)
                            self.app.quit()

        elif self.current_screen == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for slider in self.settings_sliders:
                    if slider.is_clicked(event.pos):
                        self.sound_manager.play_sound_effect("click")
                        slider.move_knob(event.pos)
                        if slider.data == "music_volume":
                            self.sound_manager.music_volume = slider.value / 100
                        if slider.data == "sound_effect_volume":
                            self.sound_manager.sound_effect_volume = slider.value / 100
                for button in self.settings_buttons:
                    if button.is_clicked(event.pos):
                        if button.data == "save":
                            self.sound_manager.play_sound_effect("save")
                            self.app.switch_screen("menu")
                        if button.data == "quit":
                            self.sound_manager.play_sound_effect("click_main_menu")
                            self.restore_settings()
                            self.app.switch_screen("menu")

    def restore_settings(self):
        self.sound_manager.music_volume = self.initial_settings_values["music_volume"]
        self.sound_manager.sound_effect_volume = self.initial_settings_values["sound_effect_volume"]
