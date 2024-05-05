import logging
import time

from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn
from Player import Player
from Game import Game
import pygame

white_player = Player('white', [], [])
black_player = Player('black', [], [])
white_player.initialize_player()
black_player.initialize_player()
game = Game(white_player, black_player)
# game.draw_turn('white')
# pygame.display.flip()
# count = 0
# for piece in white_player.pieces:
#     count += 1
#     print(f" white = piece type is : {piece.type} and his position is {piece.position}")
# print (f"num of white pieces : {count}")
# count = 0
# for piece in black_player.pieces:
#     count += 1
#     print(f" black = piece type is : {piece.type} and his position is {piece.position}")
# print (f"num of black pieces : {count}")
# time.sleep(10)
game.run_game()
game.draw_turn('white')

