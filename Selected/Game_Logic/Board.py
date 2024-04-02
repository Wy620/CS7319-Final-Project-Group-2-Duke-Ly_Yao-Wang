import pygame
import numpy as np
from pygame import surface

COL = 10
ROW = 25
SIZE = 30
Score_field = 6
Color_edge = "#4c4c4c"
class Board():
    def __init__(self):
        super().__init__()
        self.board = np.zeros((ROW,COL))

    def Load_Game(self, surface):
        for i in range (ROW):
            for j in range (COL):
                if self.board[i][j] == 0:
                    pygame.draw.rect(surface, Color_edge, (j*SIZE, i*SIZE, SIZE-1, SIZE-1))


    def Update(self,surface):
        self.Load_Game(surface)
