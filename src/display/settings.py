

import pygame
from constants import MAIN_MENU_BUTTONS_X, MAIN_MENU_SLIDERS_X, Colors, Paths, Sizes
from display.base import BaseScreen
from utils.widgets import ImageButton, Slider


class SettingsScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(name="settings", app=app, screen=screen)
        self.initials_values = {
            "music_volume": self.sound_manager.music_volume,
            "sound_effect_volume": self.sound_manager.sound_effect_volume
            }
        self.sound_manager.load_sound_effect("click", Paths.SOUND_EFFECTS / "click.mp3")
        self.sound_manager.load_sound_effect("click_main_menu", Paths.SOUND_EFFECTS / "click_main_menu.mp3")
        self.sound_manager.load_sound_effect("save", Paths.SOUND_EFFECTS / "save_grid.mp3")

        self.sliders = [
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

        self.main_buttons = [
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
        self.current_screen = "main"

    def draw_main(self):
        super().draw_main()
        for slider in self.sliders:
            slider.draw()

    def update(self):
        if self.current_screen == "main":
            self.draw_main()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for slider in self.sliders:
                if slider.is_clicked(event.pos):
                    self.sound_manager.play_sound_effect("click")
                    slider.move_knob(event.pos)
                    if slider.data == "music_volume":
                        self.sound_manager.music_volume = slider.value / 100
                    if slider.data == "sound_effect_volume":
                        self.sound_manager.sound_effect_volume = slider.value / 100
            for button in self.main_buttons:
                if button.is_clicked(event.pos):
                    if button.data == "save":
                        self.sound_manager.play_sound_effect("save")
                        self.app.switch_screen("menu")
                    if button.data == "quit":
                        self.sound_manager.play_sound_effect("click_main_menu")
                        self.restore_settings()
                        self.app.switch_screen("menu")
                
    def restore_settings(self):
        self.sound_manager.music_volume = self.initials_values["music_volume"]
        self.sound_manager.sound_effect_volume = self.initials_values["sound_effect_volume"]
