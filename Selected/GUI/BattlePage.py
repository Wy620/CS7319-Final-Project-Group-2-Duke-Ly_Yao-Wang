import pygame
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

# Next shape box dimensions
NEXT_SHAPE_BOX_SIZE = 30
NEXT_SHAPE_TEXT_OFFSET = 10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Start Page")


# Function to draw buttons
def draw_button(screen, x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


# Function to draw next shape box
def draw_next_shape_box(screen, x, y):
    pygame.draw.rect(screen, GRAY, (x, y, NEXT_SHAPE_BOX_SIZE, NEXT_SHAPE_BOX_SIZE), 1)


# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw Tetris grids (placeholders)
    pygame.draw.rect(screen, GRAY, (25, 50, 10 * 15, 20 * 15))
    pygame.draw.rect(screen, GRAY, (425, 50, 10 * 15, 20 * 15))

    # Draw vertical line in the middle
    pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

    # Draw "Next Shape" text and box on left side
    next_shape_text = pygame.font.Font(None, 24).render("Next Shape", True, BLACK)
    screen.blit(next_shape_text, (250, 50))
    draw_next_shape_box(screen, 300, 75)

    # Draw "Next Shape" text and box on right side
    next_shape_text = pygame.font.Font(None, 24).render("Next Shape", True, BLACK)
    screen.blit(next_shape_text, (SCREEN_WIDTH // 2 + 250, 50))
    draw_next_shape_box(screen, SCREEN_WIDTH // 2 + 300, 75)

    # Draw "Player 1 Points" text on left side
    next_shape_text = pygame.font.Font(None, 24).render("Player 1 Points", True, BLACK)
    screen.blit(next_shape_text, (250, 250))

    # Draw "Player 2 Points" text on right side
    next_shape_text = pygame.font.Font(None, 24).render("Player 2 Points", True, BLACK)
    screen.blit(next_shape_text, (SCREEN_WIDTH // 2 + 250, 250))

    pygame.display.flip()

    # Here you can integrate your game logic
    if GAME_ON:
        screen.fill(WHITE)
        # Main_Window.fill("#ffffff")
        Game_Board.Update(screen)
        # my_tetrimino.Draw(Main_Window,my_tetrimino.tetrimino,'red',my_tetrimino.rotation)
        my_tetrimino.update(screen, my_tetrimino.tetrimino, 'red', my_tetrimino.rotation)
        pygame.display.update()
        if Game_Board.Game_Over():
            GAME_ON = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
sys.exit()
