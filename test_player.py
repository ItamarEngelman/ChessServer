import time

import pygame
from Player import Player
from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from constants import *
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

white_player = Player('white')
black_player = Player('black')

king = King('assets/images/white king.png',  (5, 3), 'white')
#rook = Rook('assets/images/white rook.png', (3, 3), 'white')
#white_player.add_piece(rook)

rook_lst = white_player.get_pieces_by_type('Rook')
for rook in rook_lst:
    print(rook.position)
king.update_valid_moves(white_player, white_player)
print(king.valid_moves)


def draw_board(): #game
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, 800, WIDTH - 200, 100])
            pygame.draw.rect(screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
            screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))
screen.fill('light gray')
draw_board()
king.draw(screen)
rook.draw(screen)
white_player.draw_pieces(screen)
black_player.draw_pieces(screen)

pygame.display.flip()
time.sleep(1000)
pygame.quit()
