from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Pawn import Pawn
from pieces.King import King

class TestPieces:
    def __init__(self):
        self.test_bishop()
        self.test_knight()
        self.test_queen()
        self.test_rook()
        self.test_pawn()
        self.test_king()

    def test_bishop(self):
        print("Testing Bishop")
        bishop_white = Bishop((2, 0), 'white')
        bishop_black = Bishop((2, 7), 'black')
        self.print_piece_info(bishop_white)
        self.print_piece_info(bishop_black)

    def test_knight(self):
        print("Testing Knight")
        knight_white = Knight((1, 0), 'white')
        knight_black = Knight((1, 7), 'black')
        self.print_piece_info(knight_white)
        self.print_piece_info(knight_black)

    def test_queen(self):
        print("Testing Queen")
        queen_white = Queen((3, 0), 'white')
        queen_black = Queen((3, 7), 'black')
        self.print_piece_info(queen_white)
        self.print_piece_info(queen_black)

    def test_rook(self):
        print("Testing Rook")
        rook_white = Rook((0, 0), 'white')
        rook_black = Rook((0, 7), 'black')
        self.print_piece_info(rook_white)
        self.print_piece_info(rook_black)

    def test_pawn(self):
        print("Testing Pawn")
        pawn_white = Pawn((0, 1), 'white')
        pawn_black = Pawn((0, 6), 'black')
        self.print_piece_info(pawn_white)
        self.print_piece_info(pawn_black)

    def test_king(self):
        print("Testing King")
        king_white = King((4, 0), 'white')
        king_black = King((4, 7), 'black')
        self.print_piece_info(king_white)
        self.print_piece_info(king_black)

    def print_piece_info(self, piece):
        print(f"{piece.type} at {piece.position} with color {piece.color} and image path {piece.image_path}")

if __name__ == "__main__":
    TestPieces()
