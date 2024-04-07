import pygame

class WaitingToJoinPage:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            text = self.font.render("Waiting to join...", True, (0, 0, 0))
            text_rect = text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(30)

        pygame.quit()