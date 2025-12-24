import numpy as np
import pygame
import sys
import math
import time

# -------------------- CONSTANTS --------------------
ROWS = 3
COLUMNS = 3
SQUARE_SIZE = 200
WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
X_WIDTH = 25
OFFSET = 55
LINE_WIDTH = 10

# Colors
BACKGROUND_COLOR = (255, 255, 0)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 105, 180)
X_COLOR = (255, 0, 0)

# -------------------- INITIALIZATION --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - PythonGeeks")
screen.fill(BACKGROUND_COLOR)

board = np.zeros((ROWS, COLUMNS))
player = 1
game_over = False

# -------------------- FUNCTIONS --------------------
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                     int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH
                )
            elif board[row][col] == 2:
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET),
                    (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET),
                    X_WIDTH
                )
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET),
                    (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET),
                    X_WIDTH
                )

def available_square(row, col):
    return board[row][col] == 0

def mark_square(row, col, player):
    board[row][col] = player

def board_full():
    return not np.any(board == 0)

# -------------------- WIN CHECKS --------------------
def check_win(player):
    return vertical_win(player) or horizontal_win(player) or diagonal_win(player)

def vertical_win(player):
    for col in range(COLUMNS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_vertical_line(col, player)
            return True
    return False

def horizontal_win(player):
    for row in range(ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_horizontal_line(row, player)
            return True
    return False

def diagonal_win(player):
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_diagonal_line(player)
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        draw_diagonal_line(player, False)
        return True
    return False

# -------------------- WIN LINES --------------------
def draw_vertical_line(col, player):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else X_COLOR
    pygame.draw.line(screen, color, (x, 10), (x, HEIGHT - 10), CIRCLE_WIDTH)

def draw_horizontal_line(row, player):
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else X_COLOR
    pygame.draw.line(screen, color, (10, y), (WIDTH - 10, y), CIRCLE_WIDTH)

def draw_diagonal_line(player, down=True):
    color = CIRCLE_COLOR if player == 1 else X_COLOR
    if down:
        pygame.draw.line(screen, color, (25, 25), (WIDTH - 25, HEIGHT - 25), X_WIDTH)
    else:
        pygame.draw.line(screen, color, (25, HEIGHT - 25), (WIDTH - 25, 25), X_WIDTH)

# -------------------- RESET GAME --------------------
def reset_game():
    global board, player, game_over
    time.sleep(1.5)
    board = np.zeros((ROWS, COLUMNS))
    player = 1
    game_over = False
    screen.fill(BACKGROUND_COLOR)
    draw_lines()

# -------------------- MAIN LOOP --------------------
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            clicked_row = int(math.floor(mouse_y / SQUARE_SIZE))
            clicked_col = int(math.floor(mouse_x / SQUARE_SIZE))

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)

                if check_win(player):
                    game_over = True
                    draw_figures()
                    pygame.display.update()
                    reset_game()

                elif board_full():
                    game_over = True
                    reset_game()

                player = 2 if player == 1 else 1

    draw_figures()
    pygame.display.update()
