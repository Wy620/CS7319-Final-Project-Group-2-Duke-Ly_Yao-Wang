
import pygame
import sys
from P2P import p2p

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

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect to Another Player")

# Text Input box class
class TextInputBox:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ''
        self.font = font
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = GRAY if self.active else WHITE
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, 2)
        font_surface = self.font.render(self.text, True, BLACK)
        screen.blit(font_surface, (self.rect.x + 5, self.rect.y + 5))

# Create font
font = pygame.font.Font(None, 32)

# Text input boxes
player_ip_input = TextInputBox(300, 100, 200, 32, font)
invite_code_input = TextInputBox(300, 150, 200, 32, font)

# Function to draw button
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

    # Draw "Connect to another player" text centered at the top
    connect_text = font.render("Connect to another player", True, BLACK)
    connect_rect = connect_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(connect_text, connect_rect)

    # Draw labels
    player_ip_label = font.render("Player IP:", True, BLACK)
    player_ip_rect = player_ip_label.get_rect(topleft=(50, 100))
    screen.blit(player_ip_label, player_ip_rect)

    invite_code_label = font.render("Invite Code:", True, BLACK)
    invite_code_rect = invite_code_label.get_rect(topleft=(50, 150))
    screen.blit(invite_code_label, invite_code_rect)

    # Draw input boxes
    player_ip_input.draw(screen)
    invite_code_input.draw(screen)

    # Draw "Join Battle" button
    draw_button(screen, 550, 125, 150, 50, GRAY, "Join Battle")

    # Draw "Go Back" button
    draw_button(screen, 50, 300, 150, 50, GRAY, "Back")

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks
            mouse_pos = pygame.mouse.get_pos()
            if 50 < mouse_pos[0] < 200 and 300 < mouse_pos[1] < 350:
                from StartPage import main as back_to_main

                back_to_main()
            elif 550 < mouse_pos[0] < 700 and 125 < mouse_pos[1] < 175:

                join_ip_address = player_ip_input.text
                join_invite_code = invite_code_input.text

                peer = p2p(join_ip_address, join_invite_code)
                peer.connect()

                if peer.connected:
                    print("Successfully connected to the server.")
                    initial_data = {"message": "Hello from client"}
                    peer.send_data(initial_data)
                    from Unselected.Game_Logic.BattlePage import main as battle_page

                    battle_page(peer)
                    running = False
                else:
                    print("Failed to connect to the server. Please try again.")

        player_ip_input.handle_event(event)
        invite_code_input.handle_event(event)

        pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
