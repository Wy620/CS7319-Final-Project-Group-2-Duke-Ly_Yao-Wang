import pygame
import numpy as np

COL = 10
ROW = 25
SIZE = 30
SCORE_FEILD = 6
COLOR_NONE = '#3c3c3c'
SCORE_POS = (int(COL + 0.6*SCORE_FEILD)*SIZE,2*SIZE)

class Board():
    def __init__(self):
        super().__init__()
        self.board = np.zeros((COL,ROW))
        self.score = 0


    def Load_Game(self, surface, offset_x=0):
        for j in range(COL):
            for i in range(ROW):
                x_position = j * SIZE + offset_x
                if self.board[j][i] == 0:
                    pygame.draw.rect(surface, COLOR_NONE, (x_position, i * SIZE, SIZE - 1, SIZE - 1))
                if self.board[j][i] == 1:
                    pygame.draw.rect(surface, 'red', (x_position, i * SIZE, SIZE - 1, SIZE - 1))

    def Load_Side(self, surface, offset_x=0):
        for i in range(COL, COL + SCORE_FEILD):
            for j in range(ROW):
                x_position = i * SIZE + offset_x
                pygame.draw.rect(surface, COLOR_NONE, (x_position, j * SIZE, SIZE, SIZE))

        surface.blit(self.score_font, self.score_font_rect)

    def Get_Score(self):
        score = 0
        for i in range(ROW):
            count = 0
            for j in range(COL):
                if self.board[j][i]:
                    count += 1
            if count == COL:
                for j in range(COL):
                    self.board[j][i] = 0
                score += 1
                for m in range(i,0,-1):
                    for n in range(COL):
                        self.board[n][m] = self.board[n][m-1]
        return score

    def Game_Over(self):
        for i in range(COL):
            if self.board[i][0]:
                return True

    def Restart(self):
        self.board = np.zeros((COL,ROW))
        self.score = 0

    def Update(self, surface, offset_x=0):
        self.Load_Game(surface, offset_x)
        self.score += self.Get_Score()
        self.score_font = pygame.font.Font('SmileySans-Oblique.ttf',80).render(str(self.score),True,'white')
        self.score_font_rect = self.score_font.get_rect(center = (SCORE_POS[0] + offset_x, SCORE_POS[1]))
        self.Load_Side(surface, offset_x)
        self.Get_Score()

    def Set_State(self, online_player_state):
        pass