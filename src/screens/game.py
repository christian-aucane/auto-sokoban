import time
import pygame

from build_game import Level, Player
from screens.base import BaseScreen
from solve_game import Solver
from widgets import Button
from constants import DOWN, GRID_HEIGHT, GRID_WIDTH, HEIGHT, IMAGES_DIR, LEFT, LEVEL_MENU_HEIGHT, LEVELS_DIR, RIGHT, UP, WIDTH, GREEN, YELLOW, BLUE, RED, BLACK


class GameScreen(BaseScreen):
    def __init__(self, app, screen):
        sound_effects = {
            "walk": self.load_sound_effect("game/walk.mp3"),
            "wrong_move": self.load_sound_effect("game/wrong_move.mp3"),
            "box_move": self.load_sound_effect("game/box_move.mp3"),
            "box_on_goal": self.load_sound_effect("game/box_on_goal.mp3"),
        }
        super().__init__(app=app, screen=screen, music="game.mp3", sound_effects=sound_effects)
        self.main_buttons = [Button(screen=self.screen, x=0, y=HEIGHT - 50, width=WIDTH, height=50, text="Quit", bg_color=RED, text_color=BLACK),]
        self.grids_paths = []
        for i, grid in enumerate(LEVELS_DIR.iterdir()):
            self.main_buttons.append(Button(screen=self.screen, x=0, y=i * 50, width=WIDTH, height=50, text=str(i), bg_color=GREEN, text_color=BLACK))
            self.grids_paths.append(grid)
        
        self.current_screen = "main"

        level_buttons_width = WIDTH // 4
        self.level_buttons = [
            Button(screen=self.screen, x=0, y=GRID_HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Solve", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=level_buttons_width, y=GRID_HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Cancel", bg_color=YELLOW, text_color=BLACK),
            Button(screen=self.screen, x=2 * level_buttons_width, y=GRID_HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Reset", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=3 * level_buttons_width, y=GRID_HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Quit", bg_color=RED, text_color=BLACK),
        ]

        self.level = None
        self.cell_width = 0
        self.cell_height = 0
        self.images = []

        self.solver = None
        self.solve_running = False

    def draw_main(self):
        for button in self.main_buttons:
            button.draw()

    def draw_level(self):
        for y in range(self.level.height):
            for x in range(self.level.width):
                if self.level.is_empty(x, y):
                    self.draw_cell(x, y, "empty_cell")
                elif self.level.is_wall(x, y):
                    self.draw_cell(x, y, "wall")
                elif self.level.is_goal(x, y):
                    self.draw_cell(x, y, "goal")
        
        for box in self.level.boxes:
            if box.is_on_goal:
                self.draw_cell(box.x, box.y, "box_on_goal")
            else:
                self.draw_cell(box.x, box.y, "box")
        
        if self.level.player is not None:
            if self.level.player.orientation == UP:
                self.draw_cell(self.level.player.x, self.level.player.y, "player_up")
            elif self.level.player.orientation == DOWN:
                self.draw_cell(self.level.player.x, self.level.player.y, "player_down")
            elif self.level.player.orientation == LEFT:
                self.draw_cell(self.level.player.x, self.level.player.y, "player_left")
            elif self.level.player.orientation == RIGHT:
                self.draw_cell(self.level.player.x, self.level.player.y, "player_right")

        for button in self.level_buttons:
            button.draw()

    def update(self):
        if self.current_screen == "main":
        # TODO : Ajouter une image de fond
            self.draw_main()
        elif self.current_screen == "level":
            if self.solve_running:
                self.solver.apply_next_move()
                time.sleep(0.2)
            self.draw_level()

    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Quit":
                            self.app.switch_screen("menu")
                        else:
                            level_path = self.grids_paths[int(button.text)]
                            self.load_level(level_path)
        elif self.current_screen == "level":
            if event.type == pygame.KEYDOWN:
                # TODO : déplacer dans une fonction qui gère les effets sonores
                movement = None
                if event.key == pygame.K_UP:
                    movement = self.level.player.up()
                elif event.key == pygame.K_DOWN:
                    movement = self.level.player.down()
                elif event.key == pygame.K_LEFT:
                    movement = self.level.player.left()
                elif event.key == pygame.K_RIGHT:
                    movement = self.level.player.right()
                
                if movement == Player.PLAYER_MOVED:
                    self.play_sound_effect("walk")
                elif movement == Player.BOX_MOVED:
                    self.play_sound_effect("walk")
                    self.play_sound_effect("box_move")
                elif movement == Player.BOX_ON_GOAL:
                    self.play_sound_effect("walk")
                    self.play_sound_effect("box_move")
                    self.play_sound_effect("box_on_goal")
                elif movement == Player.PLAYER_NOT_MOVED:
                    self.play_sound_effect("wrong_move")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.level_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Solve":
                            self.load_solve()
                        elif button.text == "Cancel":
                            self.level.cancel()
                        elif button.text == "Reset":
                            self.level.reset()
                        elif button.text == "Quit":
                            self.current_screen = "main"

    def load_level(self, level_path):
        self.current_screen = "level"
        self.level = Level(level_path)
        self.cell_width = GRID_WIDTH // self.level.width
        self.cell_height = GRID_HEIGHT // self.level.height

        self.images = {
            "wall": self.load_img("wall.png"),
            "empty_cell": self.load_img("empty_cell.png"),
            "box": self.load_img("box.png"),
            "goal": self.load_img("goal.png"),
            "box_on_goal": self.load_img("box_on_goal.png"),
            "player_up": self.load_img("player_up.png"),
            "player_down": self.load_img("player_down.png"),
            "player_left": self.load_img("player_left.png"),
            "player_right": self.load_img("player_right.png"),
        }

    def load_solve(self):
        # TODO : afficher que la résolution est en cours
        self.solver = Solver(self.level)
        self.solve_running = self.solver.solve()

    def load_img(self, filename):
        return pygame.transform.scale(pygame.image.load(IMAGES_DIR / filename), (self.cell_width, self.cell_height))
    
    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name], (x * self.cell_width, y * self.cell_height))
