import pygame

from .base import BaseScreen
from utils.widgets import ImageButton, Slider
from constants import FONT, MAIN_MENU_SLIDERS_X, Colors, Sizes, Paths, MAIN_MENU_BUTTONS_X


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
                text="Scores",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="scores"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=400,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Create",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="create"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=500,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Quit",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit"
            )
        ]
        self.current_screen = "main"

        self.sound_manager.load_sound_effect("click", Paths.SOUND_EFFECTS / "click.mp3")
        self.sound_manager.load_sound_effect("click_main_menu", Paths.SOUND_EFFECTS / "click_main_menu.mp3")
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
                text="Main Menu",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit",
            ),
        ]

        self.settings_background_image = pygame.transform.scale(
            pygame.image.load(Paths.BACKGROUND_IMAGES / "settings.png"), (Sizes.WIDTH, Sizes.HEIGHT))

        cols = self.app.score_manager.get_columns()
        score_buttons_width = Sizes.GRID_WIDTH // (len(cols))
        self.scores_buttons_filters = [
            ImageButton(
                screen=screen,
                x=i * score_buttons_width,
                y=0,
                width=score_buttons_width,
                height=30,
                text=column,
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data=column
            ) for i, column in enumerate(cols)
        ]

        self.current_filter = cols[0]
        self.current_ascending = False

        self.score_quit_button = ImageButton(
            screen=screen,
            x=MAIN_MENU_BUTTONS_X,
            y=Sizes.HEIGHT - Sizes.MAIN_MENU_BUTTON_HEIGHT * 2,
            width=Sizes.MAIN_MENU_BUTTON_WIDTH,
            height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
            text="Main Menu",
            background_image_file=Paths.MAIN_MENU_BUTTON,
            data="quit",
        )

    def load_settings(self):
        self.current_screen = "settings"
        self.initial_settings_values = {
            "music_volume": self.sound_manager.music_volume,
            "sound_effect_volume": self.sound_manager.sound_effect_volume
        }

    def draw_settings(self):
        self.screen.blit(self.settings_background_image, (0, 0))
        for button in self.settings_buttons:
            button.draw()
        for slider in self.settings_sliders:
            slider.draw()

    def restore_settings(self):
        print("Restoring settings")
        initial_music_volume = self.initial_settings_values["music_volume"]
        initial_sound_effect_volume = self.initial_settings_values["sound_effect_volume"]
        self.sound_manager.music_volume = initial_music_volume
        self.sound_manager.sound_effect_volume = initial_sound_effect_volume
        for slider in self.settings_sliders:
            if slider.data == "music_volume":
                slider.value = int(initial_music_volume * 100)
            if slider.data == "sound_effect_volume":
                slider.value = int(initial_sound_effect_volume * 100)            

    def load_scores(self):
        self.current_screen = "scores"

    def get_scores(self):
        return self.app.score_manager.get_scores(sort_by=self.current_filter, ascending=self.current_ascending)

    def draw_scores(self):
        self.draw_background_image()
        self.draw_button(self.score_quit_button)
        for button in self.scores_buttons_filters:
            is_active = button.data == self.current_filter
            self.draw_button(button, is_active=is_active)
        # TOOD : ajouter fond d'écran
        scores = self.get_scores()
        cell_width = Sizes.GRID_WIDTH // (len(scores.columns))
        cell_height = 30
        for i, col in enumerate(scores.columns):
            header_text = FONT.render(col, True, Colors.BLACK)
            header_text_rect = header_text.get_rect(topleft=(i * cell_width, Sizes.MAIN_MENU_BUTTON_HEIGHT))
            self.screen.blit(header_text, header_text_rect)
        for row_idx, row in scores.iterrows():
            y = (row_idx + 1) * cell_height + Sizes.MAIN_MENU_BUTTON_HEIGHT
            for col_idx, value in enumerate(row):
                x = col_idx* cell_width
                cell_text = FONT.render(str(value), True, Colors.BLACK)
                cell_text_rect = cell_text.get_rect(topleft=(x, y))
                self.screen.blit(cell_text, cell_text_rect)
        
    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "settings":
            self.draw_settings()
        elif self.current_screen == "scores":
            self.draw_scores()

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
                        elif button.data == "scores":
                            self.load_scores()
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
                        if button.data == "quit":
                            self.sound_manager.play_sound_effect("click_main_menu")
                            self.restore_settings()
                        self.current_screen = "main"
            elif event.type == pygame.MOUSEBUTTONUP:  
                for slider in self.settings_sliders:
                    slider.stop_dragging()
            elif event.type == pygame.MOUSEMOTION: 
                for slider in self.settings_sliders:
                    if slider.dragging:
                        slider.move_knob(event.pos)
                        if slider.data == "music_volume":
                            self.sound_manager.music_volume = slider.value / 100
                        if slider.data == "sound_effect_volume":
                            self.sound_manager.sound_effect_volume = slider.value / 100

        elif self.current_screen == "scores":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.score_quit_button.is_clicked(event.pos):
                    self.sound_manager.play_sound_effect("click_main_menu")
                    self.current_screen = "main"
                for button in self.scores_buttons_filters:
                    if button.is_clicked(event.pos):
                        self.sound_manager.play_sound_effect("click")
                        if button.data == self.current_filter:
                            self.current_ascending = not self.current_ascending
                        else:
                            self.current_ascending = False
                            self.current_filter = button.data
