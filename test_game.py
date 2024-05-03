import logging
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
game.run_game()
# game.draw_turn('white')
# print(white_player.get_pieces_by_type("King")[0])




