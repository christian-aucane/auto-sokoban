import time
import pygame

from .base import BaseScreen
from .widgets import ImageButton
from build_game import Level, Player
from game.solve_game import LevelSolver
from constants import Orientations, Sizes, Colors, Paths,\
    FONT, MAIN_MENU_BUTTONS_X


class GameScreen(BaseScreen):
    def __init__(self, app, screen):
        sound_effects = {
            "walk": self.load_sound_effect("game/walk.mp3"),
            "wrong_move": self.load_sound_effect("game/wrong_move.mp3"),
            "box_move": self.load_sound_effect("game/box_move.mp3"),
            "box_on_goal": self.load_sound_effect("game/box_on_goal.mp3"),
        }
        super().__init__(
            app=app,
            screen=screen,
            music="game.mp3",
            sound_effects=sound_effects,
            background_image_file="game.png"
        )
        
        self.main_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=Sizes.MAIN_MENU_BUTTONS_HEIGHT + i*2*Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text=path.stem.title(),
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data=path
            )
            for i, path in enumerate(Paths.LEVELS.iterdir())
        ]
        y_custom_levels_start = self.main_buttons[-1].y + Sizes.MAIN_MENU_BUTTONS_HEIGHT * 2
        self.main_buttons += [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=y_custom_levels_start + i*2*Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text=path.stem.title(),
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data=path
            )
            for i, path in enumerate(Paths.CUSTOM_LEVELS.iterdir())
        ]
        y_custom_levels_start = self.main_buttons[-1].y + Sizes.MAIN_MENU_BUTTONS_HEIGHT * 2
        self.main_buttons.append(
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=y_custom_levels_start,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Main Menu",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit"
            )
        )

        self.current_screen = "main"

        level_buttons_width = Sizes.WIDTH // 4
        self.level_buttons = [
            ImageButton(
                screen=screen,
                x=0,
                y=Sizes.GRID_HEIGHT,
                width=level_buttons_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Solve",
                background_image_file=Paths.MENU_BUTTON,
                data="solve"
            ),
            ImageButton(
                screen=screen,
                x=level_buttons_width,
                y=Sizes.GRID_HEIGHT,
                width=level_buttons_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Cancel",
                background_image_file=Paths.MENU_BUTTON,
                data="cancel"
            ),
            ImageButton(
                screen=screen,
                x=2 * level_buttons_width,
                y=Sizes.GRID_HEIGHT,
                width=level_buttons_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Reset",
                background_image_file=Paths.MENU_BUTTON,
                data="reset"
            ),
            ImageButton(
                screen=screen,
                x=3 * level_buttons_width,
                y=Sizes.GRID_HEIGHT,
                width=level_buttons_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Menu",
                background_image_file=Paths.MENU_BUTTON,
                data="quit"
            )
        ]

        self.level = None
        self.cell_width = 0
        self.cell_height = 0
        self.images = []

        self.solver = None
        self.solve_running = False

        self.level_message = ""
        self.level_message_color = Colors.BLACK

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
            if self.level.player.orientation == Orientations.UP:
                self.draw_cell(
                    self.level.player.x,
                    self.level.player.y,
                    "player_up"
                )
            elif self.level.player.orientation == Orientations.DOWN:
                self.draw_cell(
                    self.level.player.x,
                    self.level.player.y,
                    "player_down"
                )
            elif self.level.player.orientation == Orientations.LEFT:
                self.draw_cell(
                    self.level.player.x,
                    self.level.player.y,
                    "player_left"
                )
            elif self.level.player.orientation == Orientations.RIGHT:
                self.draw_cell(
                    self.level.player.x,
                    self.level.player.y,
                    "player_right"
                )

        for button in self.level_buttons:
            self.draw_button(button)
        
        moves_text_surface = FONT.render(
            f"Moves: {self.level.moves_count}",
            True,
            Colors.BLACK
        )
        moves_width = moves_text_surface.get_width()
        x_moves = moves_width
        y = Sizes.GRID_HEIGHT + Sizes.MENU_BUTTON_HEIGHT + moves_text_surface.get_height()
        moves_text_rect = moves_text_surface.get_rect(center=(x_moves, y))
        self.screen.blit(moves_text_surface, moves_text_rect)

        counter = self.level.counter

        boxes_on_goal = counter.get("boxes_on_goal")
        boxes = counter.get("boxes")
        boxes_text_surface = FONT.render(
            f"Boxes on goal: {boxes_on_goal} / {boxes}",
            True,
            Colors.BLACK
        )
        boxes_width = boxes_text_surface.get_width()
        x_boxes = x_moves + boxes_width
        boxes_text_rect = boxes_text_surface.get_rect(center=(x_boxes, y))
        self.screen.blit(boxes_text_surface, boxes_text_rect)

        message_text_surface = FONT.render(
            self.level_message,
            True,
            self.level_message_color
        )
        message_width = message_text_surface.get_width()
        x_message = moves_width + boxes_width + message_width *2
        message_text_rect = message_text_surface.get_rect(center=(x_message, y))
        self.screen.blit(message_text_surface, message_text_rect)

    def draw_victory(self):
        # TODO : ajouter le temps
        # TODO : ajouter des boutons pour recommencer et quitter et font  le score
        self.draw_text(
            text=f"Good job! Moves : {self.level.moves_count}",
            color=Colors.BLACK,
            center=(Sizes.WIDTH // 2, Sizes.HEIGHT // 2)
        )
        
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
        self.cell_width = Sizes.GRID_WIDTH // self.level.width
        self.cell_height = Sizes.GRID_HEIGHT // self.level.height

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
            self.level_message_color = Colors.GREEN
        else:
            self.level_message = "Impossible !"
            self.level_message_color = Colors.ERROR

    def load_victory(self):
        self.current_screen = "victory"

    def load_cell(self, filename):
        return pygame.transform.scale(
            pygame.image.load(Paths.CELLS_IMAGES / filename),
            (self.cell_width, self.cell_height)
        )
    
    def draw_cell(self, x, y, img_name):
        self.screen.blit(
            self.images[img_name],
            (x * self.cell_width, y * self.cell_height)
        )
