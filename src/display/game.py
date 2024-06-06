import time
import csv

import pygame

from .base import BaseScreen
from utils.widgets import ImageButton
from build_game import Level, Player
from game.solve_game import LevelSolver
from constants import Orientations, Sizes, Colors, Paths,\
    FONT, MAIN_MENU_BUTTONS_X


class GameScreen(BaseScreen):
    def __init__(self, app, screen, score_manager):
        super().__init__(
            name="game",
            app=app,
            screen=screen,
            background_image_path=Paths.BACKGROUND_IMAGES / "game.png"
        )
        self.sound_manager.load_sound_effect("walk", Paths.SOUND_EFFECTS / "walk.mp3")
        self.sound_manager.load_sound_effect("wrong_move", Paths.SOUND_EFFECTS / "wrong_move.mp3")
        self.sound_manager.load_sound_effect("box_move", Paths.SOUND_EFFECTS / "box_move.mp3")
        self.sound_manager.load_sound_effect("box_on_goal", Paths.SOUND_EFFECTS / "box_on_goal.mp3")
        self.sound_manager.load_sound_effect("victory", Paths.SOUND_EFFECTS / "victory.mp3")
        self.sound_manager.load_sound_effect("click_main_menu", Paths.SOUND_EFFECTS / "click_main_menu.mp3")
        self.sound_manager.load_sound_effect("click_play_game", Paths.SOUND_EFFECTS / "click_play_game.mp3")
        self.sound_manager.load_sound_effect("click_solve", Paths.SOUND_EFFECTS / "click_solve.mp3")
        self.sound_manager.load_sound_effect("click_cancel", Paths.SOUND_EFFECTS / "click_cancel.mp3")
        self.sound_manager.load_sound_effect("click_reset", Paths.SOUND_EFFECTS / "click_reset.mp3")
        self.sound_manager.load_sound_effect("solve_error", Paths.SOUND_EFFECTS / "solve_error.mp3")
        self.sound_manager.load_sound_effect("solved", Paths.SOUND_EFFECTS / "solved.mp3")

        self.main_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=Sizes.MAIN_MENU_BUTTON_HEIGHT + i*2*Sizes.MAIN_MENU_BUTTON_HEIGHT,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text=path.stem.title(),
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data=path
            )
            for i, path in enumerate(Paths.LEVELS.iterdir())
        ]
        y_custom_levels_start = self.main_buttons[-1].y + Sizes.MAIN_MENU_BUTTON_HEIGHT * 2
        self.main_buttons += [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=y_custom_levels_start + i*2*Sizes.MAIN_MENU_BUTTON_HEIGHT,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text=path.stem.title(),
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data=path
            )
            for i, path in enumerate(Paths.CUSTOM_LEVELS.iterdir())
        ]
        y_custom_levels_start = self.main_buttons[-1].y + Sizes.MAIN_MENU_BUTTON_HEIGHT * 2
        self.main_buttons.append(
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=y_custom_levels_start,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
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

        self.player_name = ""
        self.victory_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=Sizes.HEIGHT // 2 + 100,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Main Menu",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=Sizes.HEIGHT // 2 + 200,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Restart",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="restart"
            )
        ]

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
            orientation = self.level.player.orientation
            if orientation == Orientations.UP:
                cell_image = "player_up"
            elif orientation == Orientations.DOWN:
                cell_image = "player_down"
            elif orientation == Orientations.LEFT:
                cell_image = "player_left"
            elif orientation == Orientations.RIGHT:
                cell_image = "player_right"

            if self.level.is_goal(self.level.player.x, self.level.player.y):
                cell_image += "_on_goal"

            self.draw_cell(self.level.player.x, self.level.player.y, cell_image)

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
        self.draw_text(
            text=f"Moves : {self.level.moves_count}",
            color=Colors.BLACK,
            center=(100, 50)
        )
        self.draw_text(
            text=f"Time : {self.level.execution_time:2f}",
            color=Colors.BLACK,
            center=(100, 150)
        )
        self.draw_text(
            text="Add player name",
            color=Colors.BLACK,
            center=(Sizes.WIDTH // 2, Sizes.HEIGHT // 2 - 100)
        )
        self.draw_text(
            text=self.player_name,
            color=Colors.BLACK,
            center=(Sizes.WIDTH // 2, Sizes.HEIGHT // 2)
        )
        
        for button in self.victory_buttons:
            self.draw_button(button)

    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "level":
            if self.level.is_solved:
                self.level.stop_timer()
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
                            self.sound_manager.play_sound_effect("click_main_menu")
                            self.app.switch_screen("menu")
                        else:
                            self.sound_manager.play_sound_effect("click_play_game")
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
                            self.sound_manager.play_sound_effect("click_solve")
                            self.load_solve()
                            self.level.solve_used = True
                        elif button.data == "cancel":
                            self.sound_manager.play_sound_effect("click_cancel")
                            self.level.cancel()
                        elif button.data == "reset":
                            self.sound_manager.play_sound_effect("click_reset")
                            self.level.reset()
                        elif button.data == "quit":
                            self.sound_manager.play_sound_effect("click_main_menu")
                            self.app.switch_screen("menu")
        elif self.current_screen == "victory":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.app.score_manager.add_score(self.player_name, self.level)
                    self.player_name = ''
                    self.app.switch_screen("menu")
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.victory_buttons:
                    if button.is_clicked(event.pos):
                        if button.data == "quit":
                            self.sound_manager.play_sound_effect("click_main_menu")
                            self.app.switch_screen("menu")
                        elif button.data == "restart":
                            self.restart()
    
    
    def save_score(self):

        stats = self.level.stats
        stats["Player Name"] = self.player_name
        score_file = Paths.SCORES_FILE
        file_exists = score_file.exists()
        
        with open(score_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=stats.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(stats)

    def play_movement_sound_effect(self, movement):
        if movement == Player.PLAYER_MOVED:
            self.sound_manager.play_sound_effect("walk")
        elif movement == Player.BOX_MOVED:
            self.sound_manager.play_sound_effect("walk")
            self.sound_manager.play_sound_effect("box_move")
        elif movement == Player.BOX_ON_GOAL:
            self.sound_manager.play_sound_effect("walk")
            self.sound_manager.play_sound_effect("box_move")
            self.sound_manager.play_sound_effect("box_on_goal")
        elif movement == Player.PLAYER_NOT_MOVED:
            self.sound_manager.play_sound_effect("wrong_move")

    def restart(self):
        self.level.reset()
        self.sound_manager.play_sound_effect("click_reset")
        self.current_screen = "level"

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
            "player_up_on_goal": self.load_cell("player_up_on_goal.png"),
            "player_down_on_goal": self.load_cell("player_down_on_goal.png"),
            "player_left_on_goal": self.load_cell("player_left_on_goal.png"),
            "player_right_on_goal": self.load_cell("player_right_on_goal.png"),
        }

    def load_solve(self):
        self.level_message = "Solving ..."
        self.update()
        pygame.display.flip()
        self.solver = LevelSolver(self.level)
        self.solve_running = self.solver.solve()
        self.sound_manager.play_sound_effect("click_solve")    
        if self.solve_running:     
            self.sound_manager.play_sound_effect("solved")
            self.level_message = "Solved !"
            self.level_message_color = Colors.GREEN
        else:
            self.sound_manager.play_sound_effect("solve_error")
            self.level_message = "Impossible !"
            self.level_message_color = Colors.ERROR

    def load_victory(self):
        self.current_screen = "victory"
        self.sound_manager.play_sound_effect("victory")

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
