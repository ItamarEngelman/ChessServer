import time

from Player import Player
from pieces.King import King
from constants import *
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

white_player = Player('white')
black_player = Player('black')

king = King('assets/images/white king.png',  (5, 3), 'white')


rook_lst = white_player.get_pieces_by_type('Rook')
for rook in rook_lst:
    print(rook.position)
king.update_valid_moves(white_player, white_player)
print(king.valid_moves)


screen.fill('light gray')
king.draw(screen)
rook.draw(screen)
white_player.draw_pieces(screen)
black_player.draw_pieces(screen)

pygame.display.flip()
time.sleep(1000)
pygame.quit()
