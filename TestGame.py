
from pieces import Bishop, Knight, Queen, Rook, Pawn, King
from Game import *

class TestGame:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.run_tests()

    def run_tests(self):
        self.test_game_creation()
        self.test_draw_board()
        self.test_move_execution()
        self.test_stalemate()
        self.test_checkmate()

    def test_game_creation(self):
        print("Testing Game Creation")
        white_player = Player("white", [], [])
        black_player = Player("black", [], [])
        game = Game(white_player, black_player, "white")
        assert game.white_player.color == "white", "White player's color should be white"
        assert game.black_player.color == "black", "Black player's color should be black"
        print("Game Creation: Passed")

    def test_draw_board(self):
        print("Testing Draw Board")
        white_player = Player("white", [], [])
        black_player = Player("black", [], [])
        game = Game(white_player, black_player, "white")
        game.draw_board()
        pygame.display.flip()
        print("Draw Board: Passed")

    def test_move_execution(self):
        print("Testing Move Execution")
        white_player = Player("white", [], [])
        black_player = Player("black", [], [])
        white_king = King((4, 0), 'white')
        black_king = King((4, 7), 'black')
        white_rook = Rook((0, 0), 'white')
        black_rook = Rook((0, 7), 'black')
        white_player.add_piece(white_king)
        white_player.add_piece(white_rook)
        black_player.add_piece(black_king)
        black_player.add_piece(black_rook)
        game = Game(white_player, black_player, "white")
        game.chose_piece((4, 0), white_player, black_player)  # בחירת החתיכה לפני ביצוע המהלך
        game.execute_move((4, 1), white_player, black_player)
        assert white_king.position == (4, 1), "White king should be at position (4, 1)"
        print("Move Execution: Passed")

    def test_stalemate(self):
        print("Testing Stalemate")
        white_player = Player("white", [], [])
        black_player = Player("black", [], [])
        white_king = King((0, 0), 'white')
        black_king = King((7, 7), 'black')
        black_rook1 = Rook((5, 6), 'black')
        black_rook2 = Rook((6, 5), 'black')
        white_player.add_piece(white_king)
        black_player.add_piece(black_king)
        black_player.add_piece(black_rook1)
        black_player.add_piece(black_rook2)
        game = Game(white_player, black_player, "white")
        game.check_game_status(white_player, black_player)
        assert game.game_over is True, "Game should be over (stalemate)"
        print("Stalemate: Passed")


if __name__ == "__main__":
    TestGame()