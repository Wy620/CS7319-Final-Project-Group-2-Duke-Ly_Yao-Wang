import pygame
import sys

image = pygame.image.load('sample.png')
image = pygame.transform.scale(image, (150, 300))
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

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw Tetris grid (placeholder)
    pygame.draw.rect(screen, GRAY, (100, 50, 10 * 15, 20 * 15))
    image_x, image_y = 100, 50  # Replace with desired position
    screen.blit(image, (image_x, image_y))


    # Draw buttons
    draw_button(screen, 500, 150, BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, "Start a Game")
    draw_button(screen, 500, 225, BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, "Join a Game")
    draw_button(screen, 500, 300, BUTTON_WIDTH, BUTTON_HEIGHT, RED, "Exit")

    # Draw "Tetris Online" text
    font = pygame.font.Font(None, 50)
    text_surface = font.render("Tetris Online", True, BLACK)
    text_rect = text_surface.get_rect(center=(500 + BUTTON_WIDTH / 2, 75))
    screen.blit(text_surface, text_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 500 < mouse_pos[0] < 500 + BUTTON_WIDTH:
                if 150 < mouse_pos[1] < 150 + BUTTON_HEIGHT:
                    print("Starting a new game...")
                    from Unselected.Game_Logic.CreateGamePage import main as create_game_main
                    create_game_main()
                elif 225 < mouse_pos[1] < 225 + BUTTON_HEIGHT:
                    print("Joining a game...")
                    from Unselected.Game_Logic.PlayerConnectPage import main as join_game_main
                    join_game_main()
                elif 300 < mouse_pos[1] < 300 + BUTTON_HEIGHT:
                    running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
