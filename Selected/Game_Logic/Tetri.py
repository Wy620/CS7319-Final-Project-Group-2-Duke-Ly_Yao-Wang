import pygame.draw
from Tetris_Block import L, Tetrimino_blocks
from Board import SIZE, ROW
import random

class Tetrimino():
    def __init__(self) -> None:
        super().__init__()
        self.tetrimino = random.choice(Tetrimino_blocks)
        self.position = 3
        self.rotation = 0
        self.speed = 0

    def Draw(self, surface, tetrimino, color, rotation):
        for i in range(len(tetrimino[rotation][0])):
            for j in range(len(tetrimino[rotation])):
                if tetrimino[rotation][i][j] == '1':
                    pygame.draw.rect(surface, color, ((j+self.position) * SIZE, (i+self.speed) * SIZE, SIZE - 1, SIZE - 1))

                if (i+self.speed) > ROW: #bring the new block when hit the end
                    self.Next_round()

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.speed += 1

    def Left_index(self, tetrimino, rotation): #left boundary
        for i in range(len(tetrimino[rotation][0])):
            for j in range(len(tetrimino[rotation])):
                if tetrimino[rotation][i][j] == '1':
                    return (i)
                
    def Right_index(self, tetrimino,rotation): #right bpundary
        for i in range(len(tetrimino[rotation][0])):
            for j in range(len(tetrimino[rotation])):
                if tetrimino[rotation][i][j] == '1':
                    right = j
        return right

    def Next_round(self):
        self.tetrimino = random.choice(Tetrimino_blocks)
        self.position = 3
        self.rotation = 0
        self.speed = 0