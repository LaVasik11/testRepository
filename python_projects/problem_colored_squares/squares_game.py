import pygame
import sys
import random
import time

pygame.init()

SCREEN_SIZE = 600
GRID_SIZE = 6
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
PADDING = 5
COOLDOWN = 0.3


COLORS = ["red", "lime", "blue", "yellow", "violet", "grey"]
COLOR_RGB = {
    "red": (255, 0, 0),
    "lime": (77, 222, 29),
    "blue": (37, 79, 194),
    "yellow": (220, 235, 16),
    "violet": (222, 22, 240),
    "grey": (105, 118, 122),
}

color_list = COLORS * 6
random.shuffle(color_list)

grid = []
for i in range(GRID_SIZE):
    row = []
    for j in range(GRID_SIZE):
        row.append(color_list.pop())
    grid.append(row)


screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("squares game")


def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = COLOR_RGB[grid[i][j]]
            rect = pygame.Rect(
                j * CELL_SIZE + PADDING,
                i * CELL_SIZE + PADDING,
                CELL_SIZE - 2 * PADDING,
                CELL_SIZE - 2 * PADDING
            )
            pygame.draw.rect(screen, color, rect)

def move_row(row, direction):
    if direction == 'left':
        grid[row] = grid[row][1:] + grid[row][:1]
    elif direction == 'right':
        grid[row] = grid[row][-1:] + grid[row][:-1]

def move_column(col, direction):
    if direction == 'up':
        first_element = grid[0][col]
        for i in range(GRID_SIZE - 1):
            grid[i][col] = grid[i + 1][col]
        grid[GRID_SIZE - 1][col] = first_element
    elif direction == 'down':
        last_element = grid[GRID_SIZE - 1][col]
        for i in range(GRID_SIZE - 1, 0, -1):
            grid[i][col] = grid[i - 1][col]
        grid[0][col] = last_element

def main():
    clock = pygame.time.Clock()
    dragging = False
    drag_start = None
    drag_direction = None
    last_move_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                dragging = True
                drag_start = (row, col)
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                drag_start = None
                drag_direction = None
            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE

                if drag_start and time.time() - last_move_time >= COOLDOWN:
                    start_row, start_col = drag_start

                    if drag_direction is None:
                        if abs(x - start_col * CELL_SIZE) > abs(y - start_row * CELL_SIZE):
                            drag_direction = 'horizontal'
                        else:
                            drag_direction = 'vertical'

                    if drag_direction == 'horizontal':
                        if col > start_col:
                            move_row(start_row, 'right')
                            last_move_time = time.time()
                        elif col < start_col:
                            move_row(start_row, 'left')
                            last_move_time = time.time()
                        drag_start = (start_row, col)
                    elif drag_direction == 'vertical':
                        if row > start_row:
                            move_column(start_col, 'down')
                            last_move_time = time.time()
                        elif row < start_row:
                            move_column(start_col, 'up')
                            last_move_time = time.time()
                        drag_start = (row, start_col)

        screen.fill((0, 0, 0))
        draw_grid()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
