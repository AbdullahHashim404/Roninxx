import sys
import pygame
import numpy as np
pygame.init()

#Colors, Proportions & Sizes
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SEMI_WHITE = (208, 208, 208, 128)
SEMI_BLACK = (0, 0, 0, 94)
LOGICAL_HEIGHT = 750  # Logical height for game calculations
STATUS_BAR_HEIGHT = 50  # Fixed height for the status bar
HEIGHT = LOGICAL_HEIGHT + STATUS_BAR_HEIGHT  # Total screen height
WIDTH = 800
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
Difficulty = ""


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')


BACKGROUND_IMAGE = pygame.image.load('bg.jpg')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))# Scale to fit screen


SCREEN.fill(WHITE)
BOARD = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color = SEMI_WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(SCREEN, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(SCREEN, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, LOGICAL_HEIGHT), LINE_WIDTH)

def draw_figures(color = [RED, BLACK]):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if BOARD[row][col] == 1:
                pygame.draw.circle(SCREEN, color[0], (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), SQUARE_SIZE // 3, 15)
            elif BOARD[row][col] == 2:
                pygame.draw.line(SCREEN, color[1], (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), 25)
                pygame.draw.line(SCREEN, color[1], (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 25)


def mark_square(row, col, player):
    BOARD[row][col] = player

def available_square(row, col):
    return BOARD[row][col] == 0

def is_board_full(check_board = BOARD):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board = BOARD):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

def minimax(minimax_board, depth, max_depth, is_maximizing):
    if check_win(2, minimax_board):
        return 10 - depth  # Favor quicker wins
    elif check_win(1, minimax_board):
        return depth - 10  # Favor slower losses
    elif is_board_full(minimax_board) or depth == max_depth:
        return 0  # Neutral score for a draw or max depth reached
    
    if is_maximizing:
        best_score = float('-inf')  # Start with the worst score
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2  # Player 2's move
                    score = minimax(minimax_board, depth + 1, max_depth, False)
                    minimax_board[row][col] = 0  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')  # Start with the best score for minimizing
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1  # Player 1's move
                    score = minimax(minimax_board, depth + 1, max_depth, True)
                    minimax_board[row][col] = 0  # Undo move
                    best_score = min(score, best_score)
        return best_score
    
def best_move(max_depth):
    best_score = float('-inf')
    move = (-1, -1)
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if BOARD[row][col] == 0:
                BOARD[row][col] = 2  # Simulate player 2's move
                score = minimax(BOARD, 0, max_depth, False)  # Call minimax with max_depth
                BOARD[row][col] = 0  # Undo the move
                
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)  # Mark the best move on the board
        return True
    return False

def welcome_screen():

    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
    custom_font = pygame.font.Font(None, 80)
    custom_title = custom_font.render('Welcome to Tic-Tac-Toe!', True, BLACK)
    custom_rect = custom_title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    SCREEN.blit(custom_title, custom_rect)
    
    font_instructions = pygame.font.Font(None, 50)
    instructions = [
        'Press 1 for Easy',
        'Press 2 for Medium',
        'Press 3 for Hard',
    ]
    
    for i, line in enumerate(instructions):
        text = font_instructions.render(line, True, SEMI_BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        SCREEN.blit(text, text_rect)
    
    pygame.display.update()

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 5

max_depth = welcome_screen()
print(f"Choosen Difficulty is {max_depth}")
SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
draw_lines()

player = 1
game_over = False

while True:

    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))  # Draw background image
    draw_lines()  # Draw game board lines
    draw_figures()  # Draw current board state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            Clicked_row = event.pos[1] // SQUARE_SIZE
            Clicked_col = event.pos[0] // SQUARE_SIZE

            if available_square(Clicked_row, Clicked_col):
                mark_square(Clicked_row, Clicked_col, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move(max_depth):
                        if check_win(2):
                            game_over = True
                    player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True


    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures([GREEN, GREEN])
            draw_lines(GREEN)
            print("You Won!")
        
        elif check_win(2):
            draw_figures([RED, RED])
            draw_lines(RED)
            print("You Loose!")
        
        else:
            draw_figures([GREY, GREY])
            draw_lines(GREY)
            print("It's a Draw!")
            
    pygame.display.update()
