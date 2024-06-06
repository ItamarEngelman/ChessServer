from Player import Player
from Game import Game

white_player = Player('white', [], [])
black_player = Player('black', [], [])
white_player.initialize_player()
black_player.initialize_player()
game = Game(white_player, black_player)


game.run_game()
game.draw_turn('white')

