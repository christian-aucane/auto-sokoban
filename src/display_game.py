from pathlib import Path
import sys
import pygame

from build_game import Grid
from constants import WIDTH, HEIGHT, WHITE, UP, DOWN, LEFT, RIGHT, IMAGES_DIR


class SokobanApp:
    def __init__(self, grid_path):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sokoban")
        self.running = True
        self.grid = Grid(grid_path)
        self.cell_width = WIDTH // self.grid.width
        self.cell_height = HEIGHT // self.grid.height
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


    def load_img(self, path):
        return pygame.transform.scale(pygame.image.load(path), (self.cell_width, self.cell_height))

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name], (x * self.cell_width, y * self.cell_height))

    def update(self):
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

        pygame.display.flip()

    def handle_keydown(self, key):
        if key == pygame.K_UP:
            self.grid.player.up()
        elif key == pygame.K_DOWN:
            self.grid.player.down()
        elif key == pygame.K_LEFT:
            self.grid.player.left()
        elif key == pygame.K_RIGHT:
            self.grid.player.right()

        elif key == pygame.K_BACKSPACE:
            self.grid.reset()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)

            self.update()


if __name__ == "__main__":
    grid_path = Path(__file__).resolve().parent / "grid" / "grid.txt"
    app = SokobanApp(grid_path)
    app.run()
