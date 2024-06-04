import time
import pygame

from .base import BaseScreen
from .widgets import ImageButton
from build_game import Level, Player
from game.solve_game import LevelSolver
from constants import CELLS_IMAGES_DIR, CUSTOM_LEVELS_DIR, DOWN, FONT_PATH, GRID_HEIGHT, GRID_WIDTH, HEIGHT, LEFT, MAIN_MENU_BUTTON_PATH, MAIN_MENU_BUTTONS_HEIGHT, MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_X, MENU_BUTTON_HEIGHT, LEVELS_DIR, MENU_BUTTON_PATH, RIGHT, UP, WIDTH, GREEN, RED, BLACK


class GameScreen(BaseScreen):
    def __init__(self, app, screen):
        sound_effects = {
            "walk": self.load_sound_effect("game/walk.mp3"),
            "wrong_move": self.load_sound_effect("game/wrong_move.mp3"),
            "box_move": self.load_sound_effect("game/box_move.mp3"),
            "box_on_goal": self.load_sound_effect("game/box_on_goal.mp3"),
        }
        super().__init__(app=app, screen=screen, music="game.mp3", sound_effects=sound_effects, background_image_file="game.png")
        
        self.main_buttons = [
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=MAIN_MENU_BUTTONS_HEIGHT + i*2*MAIN_MENU_BUTTONS_HEIGHT, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text=path.stem.title(), background_image_file=MAIN_MENU_BUTTON_PATH, data=path)
            for i, path in enumerate(LEVELS_DIR.iterdir())
        ]
        y_custom_levels_start = self.main_buttons[-1].y + MAIN_MENU_BUTTONS_HEIGHT * 2
        self.main_buttons += [
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_custom_levels_start + i*2*MAIN_MENU_BUTTONS_HEIGHT, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text=path.stem.title(), background_image_file=MAIN_MENU_BUTTON_PATH, data=path)
            for i, path in enumerate(CUSTOM_LEVELS_DIR.iterdir())
        ]
        y_custom_levels_start = self.main_buttons[-1].y + MAIN_MENU_BUTTONS_HEIGHT * 2
        self.main_buttons.append(ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_custom_levels_start, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Main Menu", background_image_file=MAIN_MENU_BUTTON_PATH, data="quit"))

        self.current_screen = "main"

        level_buttons_width = WIDTH // 4
        self.level_buttons = [
            ImageButton(screen=screen, x=0, y=GRID_HEIGHT, width=level_buttons_width, height=MENU_BUTTON_HEIGHT, text="Solve", background_image_file=MENU_BUTTON_PATH, data="solve"),
            ImageButton(screen=screen, x=level_buttons_width, y=GRID_HEIGHT, width=level_buttons_width, height=MENU_BUTTON_HEIGHT, text="Cancel", background_image_file=MENU_BUTTON_PATH, data="cancel"),
            ImageButton(screen=screen, x=2 * level_buttons_width, y=GRID_HEIGHT, width=level_buttons_width, height=MENU_BUTTON_HEIGHT, text="Reset", background_image_file=MENU_BUTTON_PATH, data="reset"),
            ImageButton(screen=screen, x=3 * level_buttons_width, y=GRID_HEIGHT, width=level_buttons_width, height=MENU_BUTTON_HEIGHT, text="Menu", background_image_file=MENU_BUTTON_PATH, data="quit")
        ]

        self.level = None
        self.cell_width = 0
        self.cell_height = 0
        self.images = []

        self.solver = None
        self.solve_running = False

        self.level_message = ""
        self.level_message_color = BLACK

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

        font = pygame.font.Font(FONT_PATH, 30)
        
        moves_text_surface = font.render(f"Moves: {self.level.moves_count}", True, BLACK)
        moves_width = moves_text_surface.get_width()
        x_moves = moves_width
        y = GRID_HEIGHT + MENU_BUTTON_HEIGHT + moves_text_surface.get_height()
        moves_text_rect = moves_text_surface.get_rect(center=(x_moves, y))
        self.screen.blit(moves_text_surface, moves_text_rect)

        counter = self.level.counter

        boxes_on_goal = counter.get("boxes_on_goal")
        boxes = counter.get("boxes")
        boxes_text_surface = font.render(f"Boxes on goal: {boxes_on_goal} / {boxes}", True, BLACK)
        boxes_width = boxes_text_surface.get_width()
        x_boxes = x_moves + boxes_width
        boxes_text_rect = boxes_text_surface.get_rect(center=(x_boxes, y))
        self.screen.blit(boxes_text_surface, boxes_text_rect)

        message_text_surface = font.render(self.level_message, True, self.level_message_color)
        message_width = message_text_surface.get_width()
        x_message = moves_width + boxes_width + message_width *2
        message_text_rect = message_text_surface.get_rect(center=(x_message, y))
        self.screen.blit(message_text_surface, message_text_rect)

    def draw_victory(self):
        # TODO : ajouter le temps
        # TODO : ajouter des boutons
        
        font = pygame.font.Font(FONT_PATH, 30)
        text = f"Good job! Moves : {self.level.moves_count}"
        message_text_surface = font.render(text, True, BLACK)
        
        message_text_rect = message_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_text_surface, message_text_rect)

    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "level":
            if self.level.is_solved:
                self.load_victory()
            if self.solve_running:
                self.solver.apply_next_move()
                time.sleep(0.2)
            self.draw_level()
        elif self.current_screen == "victory":
            self.draw_victory()

    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        if button.data == "quit":
                            self.app.switch_screen("menu")
                        else:
                            self.load_level(button.data)

        elif self.current_screen == "level":
            if event.type == pygame.KEYDOWN:
                movement = None
                if event.key == pygame.K_UP:
                    movement = self.level.player.up()
                elif event.key == pygame.K_DOWN:
                    movement = self.level.player.down()
                elif event.key == pygame.K_LEFT:
                    movement = self.level.player.left()
                elif event.key == pygame.K_RIGHT:
                    movement = self.level.player.right()
                
                self.play_movement_sound_effect(movement)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.level_buttons:
                    if button.is_clicked(event.pos):
                        if button.data == "solve":
                            self.load_solve()
                        elif button.data == "cancel":
                            self.level.cancel()
                        elif button.data == "reset":
                            self.level.reset()
                        elif button.data == "quit":
                            self.app.switch_screen("menu")
        elif self.current_screen == "victory":
            # TODO : ajouter les evenements pour enregistrer les scores
            if event.type == pygame.K_BACKSPACE:
                self.app.switch_screen("menu")

    def play_movement_sound_effect(self, movement):
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

    def load_level(self, level_path):
        self.current_screen = "level"
        self.level = Level.from_file(level_path)
        self.cell_width = GRID_WIDTH // self.level.width
        self.cell_height = GRID_HEIGHT // self.level.height

        self.images = {
            "wall": self.load_cell("wall.png"),
            "empty_cell": self.load_cell("empty_cell.png"),
            "box": self.load_cell("box.png"),
            "goal": self.load_cell("goal.png"),
            "box_on_goal": self.load_cell("box_on_goal.png"),
            "player_up": self.load_cell("player_up.png"),
            "player_down": self.load_cell("player_down.png"),
            "player_left": self.load_cell("player_left.png"),
            "player_right": self.load_cell("player_right.png"),
        }

    def load_solve(self):
        self.level_message = "Solving ..."
        self.update()
        pygame.display.flip()
        self.solver = LevelSolver(self.level)
        self.solve_running = self.solver.solve()
        if self.solve_running:
            self.level_message = "Solved !"
            self.level_message_color = GREEN
        else:
            self.level_message = "Impossible !"
            self.level_message_color = RED

    def load_victory(self):
        self.current_screen = "victory"

    def load_cell(self, filename):
        return pygame.transform.scale(pygame.image.load(CELLS_IMAGES_DIR / filename), (self.cell_width, self.cell_height))
    
    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name], (x * self.cell_width, y * self.cell_height))
