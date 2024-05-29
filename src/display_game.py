from pathlib import Path
import sys
import pygame
from pygame import mixer


from constants import WIDTH, HEIGHT
from screens.menu import MenuScreen

from build_game import Grid
from constants import LEVEL_MENU_HEIGHT, LEVELS_DIR, WIDTH, HEIGHT, WHITE, GREEN, RED, BLACK, BLUE, YELLOW, UP, DOWN, LEFT, RIGHT, IMAGES_DIR, HOME, LEVEL, CREATE, PLAYERS, RANKING
from Database.database import *

class Button:
    """
    Button class for creating interactive buttons on a Pygame screen.

    Args:
        screen (pygame.Surface): The screen to draw the button on.
        x (int): The x coordinate of the button.
        y (int): The y coordinate of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        text (str): The text displayed on the button.
        bg_color (tuple): The color of the button.
        text_color (tuple): The color of the text.

    Attributes:
        rect (pygame.Rect): The rectangle representing the button.
        text (str): The text displayed on the button.
        bg_color (tuple): The color of the button.
        text_color (tuple): The color of the text.
        screen (pygame.Surface): The screen to draw the button on.

    Methods:
        draw(): Draw the button on the screen.
        is_clicked(pos): Check if the button is clicked given a mouse position.
        set_bg_color(color): Change the button color.
        set_text_color(color): Change the button text color.
    """
    def __init__(self, screen, x, y, width, height, text, bg_color, text_color):
        """
        Initialize the button

        Args:
            screen (pygame.Surface): the screen to draw on
            x (int): x coordinate of the button
            y (int): y coordinate of the button
            width (int): width of the button
            height (int): height of the button
            text (str): text of the button
            bg_color (tuple): color of the button
            text_color (tuple): color of the text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.screen = screen

    def draw(self):
        """
        Draw the button on the screen
        """
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        font = pygame.font.SysFont("", 30)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Check if the button is clicked given a mouse position

        Args:
            pos (tuple): the position of the mouse

        Returns:
            bool: True if the button is clicked, False otherwise
        """
        return self.rect.collidepoint(pos)

    def set_bg_color(self, color):
        """
        Change the button color

        Args:
            color (tuple): the new color
        """
        self.bg_color = color

    def set_text_color(self, color):
        """
        Change the button text color

        Args:
            color (tuple): the new color
        """
        self.text_color = color

class TextInput:
    def __init__(self, screen, x, y, width, height, text_color, bg_color):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = text_color
        self.bg_color = bg_color
        self.text = ""

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        font = pygame.font.SysFont("", 30)
        text_surface = font.render(self.text, True, self.text_color)
        self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

class SokobanApp:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Sokoban")
        self.running = True

        self.menu = MenuScreen(self, self.screen)

        self.current_screen = self.menu
        self.current_screen.load()
        self.page = HOME
        self.current_level = 0
        self.player_name_input = TextInput(screen=self.screen, x=50, y=400, width=200, height=50, text_color=BLACK, bg_color=WHITE)
        # TODO : Centrer les boutons
        self.home_screen_buttons = [
            Button(screen=self.screen, x=50, y=100, width=200, height=50, text="Play", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=50, y=200, width=200, height=50, text="Create", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=50, y=300, width=200, height=50, text="Quit", bg_color=RED, text_color=BLACK),
            Button(screen=self.screen, x=50, y=400, width=200, height=50, text="Players", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=50, y=500, width=200, height=50, text="Ranking", bg_color=YELLOW, text_color=BLACK),
        ]
        level_buttons_width = WIDTH // 4
        # TODO : centrer les boutons
        self.level_buttons = [
            Button(screen=self.screen, x=0, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Solve", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=level_buttons_width, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Cancel", bg_color=YELLOW, text_color=BLACK),
            Button(screen=self.screen, x=2 * level_buttons_width, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Reset", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=3 * level_buttons_width, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Quit", bg_color=RED, text_color=BLACK),
        ]
        self.back_button = Button(screen=self.screen, x=50, y=50, width=100, height=30, text="Back", bg_color=RED, text_color=BLACK)

    # LEVEL
    def load_img(self, path):
        return pygame.transform.scale(pygame.image.load(path), (self.cell_width, self.cell_height))

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name], (x * self.cell_width, y * self.cell_height))

    def load_level(self, level_index):
        self.current_level = level_index
        self.page = LEVEL
        # TODO : Créer plusieurs niveaux
        grid_path = Path(__file__).parent / "levels" / f"level{level_index}.txt"
        # TODO : enlever la ligne suivante (provisoire)
        grid_path = LEVELS_DIR / f"grid.txt"
        self.grid = Grid(grid_path)
        self.cell_width = WIDTH // self.grid.width
        self.cell_height = HEIGHT // self.grid.height
        pygame.display.set_mode((WIDTH, HEIGHT + LEVEL_MENU_HEIGHT))
        # TODO : Adapted la taille de la fenetre plutot que d'adapter la taille des cellules ??

        self.images = {
            "wall": self.load_img(IMAGES_DIR / "wall.png"),
            "empty_cell": self.load_img(IMAGES_DIR / "empty_cell.png"),
            "box": self.load_img(IMAGES_DIR / "box.png"),
            "goal": self.load_img(IMAGES_DIR / "goal.png"),
            "box_on_goal": self.load_img(IMAGES_DIR / "box_on_goal.png"),
            "player_up": self.load_img(IMAGES_DIR / "player_up.png"),
            "player_down": self.load_img(IMAGES_DIR / "player_down.png"),
            "player_left": self.load_img(IMAGES_DIR / "player_left.png"),
            "player_right": self.load_img(IMAGES_DIR / "player_right.png"),
        }

    def show_level(self):
        self.screen.fill(WHITE)
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.is_empty(x, y):
                    self.draw_cell(x, y, "empty_cell")
                elif self.grid.is_wall(x, y):
                    self.draw_cell(x, y, "wall")
                elif self.grid.is_goal(x, y):
                    self.draw_cell(x, y, "goal")
        
        for box in self.grid.boxes:
            if box.is_on_goal:
                self.draw_cell(box.x, box.y, "box_on_goal")
            else:
                self.draw_cell(box.x, box.y, "box")
        
        if self.grid.player is not None:
            if self.grid.player.orientation == UP:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_up")
            elif self.grid.player.orientation == DOWN:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_down")
            elif self.grid.player.orientation == LEFT:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_left")
            elif self.grid.player.orientation == RIGHT:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_right")

        for button in self.level_buttons:
            button.draw()

    def handle_level_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.grid.player.up()
            elif event.key == pygame.K_DOWN:
                self.grid.player.down()
            elif event.key == pygame.K_LEFT:
                self.grid.player.left()
            elif event.key == pygame.K_RIGHT:
                self.grid.player.right()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.level_buttons:
                if button.is_clicked(event.pos):
                    print(button.text)
                    if button.text == "Solve":
                        self.load_solve()
                    if button.text == "Cancel":
                        self.grid.cancel()
                    elif button.text == "Reset":
                        self.grid.reset()
                    elif button.text == "Quit":
                        self.load_home()

    # HOME
    def load_home(self):
        self.page = HOME

    def show_home(self):
        # TODO : Ajouter un fond d'ecran
        # TODO : Ajouter un texte
        self.screen.fill(WHITE)

        for button in self.home_screen_buttons:
            button.draw()
    
    def handle_home_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.home_screen_buttons:
                if button.is_clicked(event.pos):
                    if button.text == "Play":
                        self.load_level(self.current_level)
                    elif button.text == "Create":
                        self.load_create()
                    elif button.text == "Quit":
                        self.quit()
                    elif button.text == "Players":
                        self.load_players()
                    elif button.text == "Ranking":
                        self.load_ranking()
    # PLAYERS
    def load_players(self):
        self.page = PLAYERS
        self.player_name_input = ""

    def show_players(self):
        self.screen.fill(WHITE)
        players = get_all_players()
        for i, player in enumerate(players):
            text_surface = pygame.font.SysFont("", 30).render(f"{player['name']}", True, BLACK)
            self.screen.blit(text_surface, (50, 100 + i * 50))
            # Ajouté un bouton "Supprimer" à côté de chaque joueur
            delete_button = Button(screen=self.screen, x=300, y=100 + i * 50, width=100, height=30, text="Delete", bg_color=RED, text_color=BLACK)
            delete_button.draw()
        # Ajouté un champ de texte et un bouton "Ajouter" pour ajouter de nouveaux joueurs
        text_surface = pygame.font.SysFont("", 30).render(self.player_name_input, True, BLACK)
        self.screen.blit(text_surface, (50, 100 + len(players) * 50))
        add_button = Button(screen=self.screen, x=300, y=100 + len(players) * 50, width=100, height=30, text="Add", bg_color=GREEN, text_color=BLACK)
        add_button.draw()
        self.back_button.draw()
        

    def handle_players_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name_input = self.player_name_input[:-1]
            else:
                self.player_name_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            players = get_all_players()
            for i, player in enumerate(players):
                delete_button = Button(screen=self.screen, x=300, y=100 + i * 50, width=100, height=30, text="Delete", bg_color=RED, text_color=BLACK)
                if delete_button.is_clicked(event.pos):
                    delete_player_by_name(player['name'])
            add_button = Button(screen=self.screen, x=300, y=100 + len(players) * 50, width=100, height=30, text="Add", bg_color=GREEN, text_color=BLACK)
            if add_button.is_clicked(event.pos):
                add_player(len(players) + 1, self.player_name_input)
                self.player_name_input = ""
            if self.back_button.is_clicked(event.pos):
                self.load_home()

    # RANKING
    def load_ranking(self):
        self.page = RANKING

    def show_ranking(self):
        self.screen.fill(WHITE)
        players = get_all_players()
        for i, player in enumerate(players):
            text_surface = pygame.font.SysFont("", 20).render(
                f"Name: {player['name']}, Successes: {player['successes']}, Last grid time: {player['last grid time']}, Last grid moves: {player['last grid moves']}", 
                True, BLACK)
            self.screen.blit(text_surface, (50, 100 + i * 50))
        self.back_button.draw()

    def handle_ranking_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event.pos):
                self.load_home()
                        
    # CREATE
    def load_create(self):
        ...

    def show_create(self):
        ...

    def handle_create_event(self, event):
        ...

    # SOLVE
    def load_solve(self):
        print("SOLVE")

    def show_solve(self):
        ...

    # MAIN
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif self.page == HOME:
            self.handle_home_event(event)
        elif self.page == CREATE:
            self.handle_create_event(event)
        elif self.page == LEVEL:
            self.handle_level_event(event)
        elif self.page == PLAYERS:
            self.handle_players_event(event)
        elif self.page == RANKING:
            self.handle_ranking_event(event)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.current_screen.handle_event(event)

            self.current_screen.update()
            self.handle_event(event)

            if self.page == HOME:
                self.show_home()
            elif self.page == CREATE:
                self.show_create()
            elif self.page == LEVEL:
                self.show_level()
            elif self.page == PLAYERS:
                self.show_players()
            elif self.page == RANKING:
                self.show_ranking()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60FPS

    def switch_screen(self, screen_name):
        self.current_screen.quit()
        if screen_name == "menu":
            self.current_screen = self.menu
        elif screen_name == "game":
            print("GAME")
        elif screen_name == "create":
            print("CREATE")
        self.current_screen.load()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    grid_path = Path(__file__).resolve().parent / "grid" / "grid.txt"
    app = SokobanApp()
    app.run()