import pygame
import sys

from Board import COL, ROW, SIZE, Score_field, Board
from Tetri import Tetrimino
from Tetris_Block import L

pygame.init()

Main_Window = pygame.display.set_mode(((COL + Score_field) * SIZE, ROW * SIZE))
Game_board = Board()
my_tetrimino = Tetrimino()
clock = pygame.time.Clock()
FPS = 30


while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #control the movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and (my_tetrimino.Left_index(my_tetrimino.tetrimino, my_tetrimino.rotation) + my_tetrimino.position) > 0: 
                #left key
                my_tetrimino.position -= 1
            if event.key == pygame.K_RIGHT and (my_tetrimino.Right_index(my_tetrimino.tetrimino, my_tetrimino.rotation) + my_tetrimino.position) < COL - 1:
                #right key
                my_tetrimino.position += 1
            if event.key == pygame.K_z: #rotation
                if my_tetrimino.tetrimino == L and my_tetrimino.rotation == 0 and (my_tetrimino.Right_index(my_tetrimino.tetrimino, my_tetrimino.rotation) + my_tetrimino.position) ==  COL - 1:
                    my_tetrimino.rotation = my_tetrimino.rotation
                elif my_tetrimino.tetrimino ==L and my_tetrimino.tetrimino ==2 and (my_tetrimino.Left_index(my_tetrimino.tetrimino, my_tetrimino.rotation) + my_tetrimino.position) == 0:
                    my_tetrimino.rotation = my_tetrimino.rotation
                else:
                    my_tetrimino.rotation += 1
                if my_tetrimino.rotation > 3:
                    my_tetrimino.rotation = 0


    Main_Window.fill("#ffffff")
    Game_board.Update(Main_Window)
    my_tetrimino.Draw(Main_Window, my_tetrimino.tetrimino, 'red', my_tetrimino.rotation)  

    pygame.display.update()
