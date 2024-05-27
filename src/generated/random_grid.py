import random
from icecream import ic


def generate_grid(width, height, num_boxes):
    # Initial empty grid
    grid = [['0' for _ in range(width)] for _ in range(height)]

    # Place walls around the edges
    for i in range(width):
        grid[0][i] = '1'
        grid[height-1][i] = '1'
    for i in range(height):
        grid[i][0] = '1'
        grid[i][width-1] = '1'

    # Randomly place boxes
    placed_boxes = 0
    while placed_boxes < num_boxes:
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if grid[y][x] == '0':
            grid[y][x] = '2'
            placed_boxes += 1

    # Randomly place goals
    location_goals = 0
    while location_goals < num_boxes:
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if grid[y][x] == '0':
            grid[y][x] = '3'
            location_goals += 1

    # Place the player
    while True:
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if grid[y][x] == '0':
            grid[y][x] = '4'
            break

    return grid


width = 10
height = 8
num_boxes = 5


def print_grid(grid):
    for row in grid:
        print(''.join(row))

print_grid(generate_grid(width, height, num_boxes))

