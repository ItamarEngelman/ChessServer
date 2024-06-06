from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Rook import Rook
from pieces.King import King
from Player import Player

class TestPlayer:
    def __init__(self):
        self.test_player_creation()
        self.test_add_piece()
        self.test_remove_piece()
        self.test_get_all_positions()
        self.test_get_all_valid_moves()
        self.test_get_pieces_by_type()
        self.test_check_check()
        self.test_update_check()
        self.test_check_mate()
        self.test_check_stale_mate()

    def test_player_creation(self):
        print("Testing Player Creation")
        player_white = Player("white", [], [])
        player_black = Player("black", [], [])
        print(f"Created Player: color={player_white.color}, pieces={len(player_white.pieces)}, captured pieces={len(player_white.capture_pieces)}")
        print(f"Created Player: color={player_black.color}, pieces={len(player_black.pieces)}, captured pieces={len(player_black.capture_pieces)}")

    def test_add_piece(self):
        print("Testing Add Piece")
        player = Player("white", [], [])
        bishop = Bishop((2, 0), 'white')
        player.add_piece(bishop)
        print(f"Player pieces after adding Bishop: {[(piece.type, piece.position) for piece in player.pieces]}")

    def test_remove_piece(self):
        print("Testing Remove Piece")
        player = Player("white", [], [])
        bishop = Bishop((2, 0), 'white')
        player.add_piece(bishop)
        player.remove_piece(bishop)
        print(f"Player pieces after removing Bishop: {[(piece.type, piece.position) for piece in player.pieces]}")

    def test_get_all_positions(self):
        print("Testing Get All Positions")
        player = Player("white", [], [])
        bishop = Bishop((2, 0), 'white')
        knight = Knight((1, 0), 'white')
        player.add_piece(bishop)
        player.add_piece(knight)
        positions = player.get_all_positions()
        print(f"All positions: {positions}")

    def test_get_all_valid_moves(self):
        print("Testing Get All Valid Moves")
        player = Player("white", [], [])
        bishop = Bishop((2, 0), 'white')
        knight = Knight((1, 0), 'white')
        player.add_piece(bishop)
        player.add_piece(knight)
        for piece in player.pieces:
            piece.update_valid_moves(player, Player("black", [], []))
        valid_moves = player.get_all_valid_moves()
        print(f"All valid moves: {valid_moves}")

    def test_get_pieces_by_type(self):
        print("Testing Get Pieces By Type")
        player = Player("white", [], [])
        bishop = Bishop((2, 0), 'white')
        knight = Knight((1, 0), 'white')
        player.add_piece(bishop)
        player.add_piece(knight)
        bishops = player.get_pieces_by_type("Bishop")
        knights = player.get_pieces_by_type("Knight")
        print(f"Bishops: {[(piece.type, piece.position) for piece in bishops]}")
        print(f"Knights: {[(piece.type, piece.position) for piece in knights]}")

    def test_check_check(self):
        print("Testing Check Check")
        player_white = Player("white", [], [])
        player_black = Player("black", [], [])
        king_white = King((4, 0), 'white')
        rook_black = Rook((4, 7), 'black')
        player_white.add_piece(king_white)
        player_black.add_piece(rook_black)
        player_white.update_check(player_black)
        print(f"White King in check: {player_white.check}")

    def test_update_check(self):
        print("Testing Update Check")
        player_white = Player("white", [], [])
        player_black = Player("black", [], [])
        king_white = King((4, 0), 'white')
        rook_black = Rook((4, 7), 'black')
        player_white.add_piece(king_white)
        player_black.add_piece(rook_black)
        player_white.update_check(player_black)
        print(f"White King in check after update: {player_white.check}")

    def test_check_mate(self):
        print("Testing Check Mate")
        player_white = Player("white", [], [])
        player_black = Player("black", [], [])
        king_white = King((4, 0), 'white')
        rook_black1 = Rook((4, 7), 'black')
        rook_black2 = Rook((5, 7), 'black')
        player_white.add_piece(king_white)
        player_black.add_piece(rook_black1)
        player_black.add_piece(rook_black2)
        player_white.update_check(player_black)
        check_mate = player_white.check_mate(player_black)
        print(f"White player in check mate: {check_mate}")

    def test_check_stale_mate(self):
        print("Testing Stale Mate")
        player_white = Player("white", [], [])
        player_black = Player("black", [], [])
        king_white = King((4, 0), 'white')
        rook_black1 = Rook((0, 7), 'black')
        rook_black2 = Rook((7, 7), 'black')
        player_white.add_piece(king_white)
        player_black.add_piece(rook_black1)
        player_black.add_piece(rook_black2)
        player_white.update_check(player_black)
        stale_mate = player_white.check_stale_mate()
        print(f"White player in stale mate: {stale_mate}")

if __name__ == "__main__":
    TestPlayer()
