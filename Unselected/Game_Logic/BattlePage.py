import sys
import pygame

from Board import ROW, COL, SIZE, SCORE_FEILD, Board, SCORE_POS
from P2P import p2p
from Tetri import Tetrimino, Game_Board
from Tetrimino_list import T, J, L, S, I, Z


class BattlePage:


    def __init__(self, peer):
        self.remote_tetrimino = Tetrimino()
        self.FPS = 60
        self.GAME_ON = True
        pygame.init()

        self.BORDER_WIDTH = 10
        self.window_width = (COL * SIZE) * 2 + (SCORE_FEILD * SIZE) * 2
        self.window_height = ROW * SIZE

        self.Main_Window = pygame.display.set_mode((self.window_width, self.window_height))
        self.NEXT_TETRIMINO_POS = (SCORE_POS[0], SCORE_POS[1] + 5)

        self.my_tetrimino = Tetrimino()
        self.my_tetrimio_1 = Tetrimino()

        self.clock = pygame.time.Clock()
        self.Online_Game_Board = Board()
        self.peer = peer

    def run(self):
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.GAME_ON:
                            self.GAME_ON = True
                            Game_Board.Restart()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if not GAME_ON:
                                GAME_ON = True
                                Game_Board.Restart()
                        if event.key == pygame.K_a and (self.my_tetrimino.Index_left(self.my_tetrimino.tetrimino,
                                                                                     self.my_tetrimino.rotation) + self.my_tetrimino.position) > 0 and not self.my_tetrimino.Coliide_left(
                            self.my_tetrimino.tetrimino, self.my_tetrimino.rotation):
                            self.my_tetrimino.position -= 1
                        if event.key == pygame.K_d and (self.my_tetrimino.Index_right(self.my_tetrimino.tetrimino,
                                                                                      self.my_tetrimino.rotation) + self.my_tetrimino.position) < COL - 1 and not self.my_tetrimino.Coliide_right(
                            self.my_tetrimino.tetrimino, self.my_tetrimino.rotation):
                            self.my_tetrimino.position += 1
                        if event.key == pygame.K_SPACE:

                            # S transform
                            if self.my_tetrimino.tetrimino == S and self.my_tetrimino.rotation == 1 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == COL - 1:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == S and self.my_tetrimino.rotation == 3 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == COL - 1:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            # Z transform
                            elif self.my_tetrimino.tetrimino == Z and self.my_tetrimino.rotation == 1 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == COL - 1:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == Z and self.my_tetrimino.rotation == 3 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == COL - 1:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            # LINE transform
                            elif self.my_tetrimino.tetrimino == I and self.my_tetrimino.rotation == 1 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position >= COL - 2:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == I and self.my_tetrimino.rotation == 1 and self.my_tetrimino.Index_left(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == 0:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == I and self.my_tetrimino.rotation == 3 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position >= COL - 2:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == I and self.my_tetrimino.rotation == 3 and self.my_tetrimino.Index_left(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == 0:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            # J transform
                            elif self.my_tetrimino.tetrimino == J and self.my_tetrimino.rotation == 0 and self.my_tetrimino.Index_left(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == 0:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == J and self.my_tetrimino.rotation == 2 and self.my_tetrimino.Index_left(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == 0:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            # L transform
                            elif self.my_tetrimino.tetrimino == L and self.my_tetrimino.rotation == 2 and self.my_tetrimino.Index_left(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == 0:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == L and self.my_tetrimino.rotation == 0 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == COL - 1:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            # T transform
                            elif self.my_tetrimino.tetrimino == T and self.my_tetrimino.rotation == 1 and self.my_tetrimino.Index_left(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == 0:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.tetrimino == T and self.my_tetrimino.rotation == 3 and self.my_tetrimino.Index_right(
                                    self.my_tetrimino.tetrimino,
                                    self.my_tetrimino.rotation) + self.my_tetrimino.position == COL - 1:
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            elif self.my_tetrimino.Coliide_rotation(self.my_tetrimino.tetrimino,
                                                                    self.my_tetrimino.rotation):
                                self.my_tetrimino.rotation = self.my_tetrimino.rotation
                            else:
                                self.my_tetrimino.rotation += 1

                            if self.my_tetrimino.rotation > 3:
                                self.my_tetrimino.rotation = 0

            if self.GAME_ON:
                self.main_game_logic()

            local_game_over = Game_Board.Game_Over()
            online_game_over = self.Online_Game_Board.Game_Over()

            if local_game_over or online_game_over:
                self.GAME_ON = False

                win = not local_game_over and online_game_over
                self.show_end_game_message(win=win)
                break


    def draw_next_tetrimino(self, surface, tetrimino):
        x, y = self.NEXT_TETRIMINO_POS

        for i, row in enumerate(tetrimino.shape[tetrimino.rotation]):
            for j, cell in enumerate(row):
                if cell == '1':
                    pygame.draw.rect(surface, "green",
                                     (x + j * SIZE - 60, y + i * SIZE + 100, SIZE - 4, SIZE - 4))

    def show_end_game_message(self, win):
        translucent_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        translucent_surface.fill((0, 0, 0, 128))

        font = pygame.font.Font(None, 72)
        if win:
            message = "You Win!"
            color = (0, 255, 0)
        else:
            message = "You Lose!"
            color = (255, 0, 0)

        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(self.window_width / 2, self.window_height / 2))
        translucent_surface.blit(text, text_rect)

        self.Main_Window.blit(translucent_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)

    def main_game_logic(self):
        self.Main_Window.fill("#ffffff")

        # Update and draw local game board on the left
        Game_Board.Update(self.Main_Window, offset_x=0)
        self.my_tetrimino.update(self.Main_Window, self.my_tetrimino.tetrimino, 'blue', self.my_tetrimino.rotation, offset_x=0)

        if self.peer.connected:
            print("Peer is connected.")
            local_state = {
                "tetrimino": {
                    "shape": self.my_tetrimino.tetrimino,
                    "position": self.my_tetrimino.position,
                    "rotation": self.my_tetrimino.rotation
                },
                "board": Game_Board.board.tolist(),
                "score": Game_Board.score,
            }
            self.peer.send_data(local_state)
            print("Sent local state.")

            remote_data = self.peer.receive_data()
            if remote_data:
                print("Received remote data:")
                self.remote_tetrimino.shape = remote_data["tetrimino"]["shape"]
                self.remote_tetrimino.position = remote_data["tetrimino"]["position"]
                self.remote_tetrimino.rotation = remote_data["tetrimino"]["rotation"]
                remote_board = remote_data["board"]
                remote_score = remote_data["score"]

                self.Online_Game_Board.board = remote_board
                self.Online_Game_Board.score = remote_score

                print("remote tetrimino position:", self.remote_tetrimino.position)
                right_side_offset = COL * SIZE + SCORE_FEILD * SIZE
                self.Online_Game_Board.Update(self.Main_Window,offset_x=right_side_offset)
                # remote_tetrimino_offset = right_side_offset
                self.remote_tetrimino.update(self.Main_Window, self.remote_tetrimino.shape, "green",self.remote_tetrimino.rotation, offset_x=16)

        pygame.display.update()

        if Game_Board.Game_Over() or self.Online_Game_Board.Game_Over():
            self.GAME_ON = False

def main(peer):
    battle_page = BattlePage(peer)
    battle_page.run()
    battle_page.main_game_logic()

if __name__ == "__main__":
    peer = p2p()
    main(peer)