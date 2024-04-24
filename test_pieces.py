import time

import pygame
from Bishop import Bishop
from King import King
from Knight import Knight
from Rook import Rook
from Queen import Queen
from Pawn import Pawn

# Initialize pygame
pygame.init()

# Testing function for each class
def test_piece(piece_class, image_path, start_pos, move_pos, name, screen):
    piece = piece_class(image_path, start_pos, 'white')
    print(f"Testing {name}...")
    print(f"Initial Position: {piece.position}, Moved: {piece.moved}")
    piece.update_position(move_pos)
    print(f"Position after moving to {move_pos}: {piece.position}")
    piece.update_moved()
    print(f"Moved state after move: {piece.moved}")
    piece.update_valid_moves()
    print(f"piece.valid.moves :{piece.valid_moves}")
    #piece.draw(screen)
    #print(f"drawed image of the piece")
    #capture_image = piece.capture_drawing()
    #screen.blit(capture_image, (piece.position[0] * 1000 / 8 + 1000 / 80, piece.position[1] * 900 / 8 + 900 / 80))
   # pygame.display.flip()
   # time.sleep(3)


# Paths for images
paths = {
    'Bishop': 'assets/images/white bishop.png',
    'King': 'assets/images/white king.png',
    'Knight': 'assets/images/white knight.png',
    'Rook': 'assets/images/white rook.png',
    'Queen': 'assets/images/white queen.png',
    'Pawn': 'assets/images/white pawn.png'
}




screen = pygame.display.set_mode([1000, 900])
test_piece(Bishop, 'assets/images/white bishop.png', (2, 0), (3, 1), 'Bishop', screen)
test_piece(King, paths['King'], (4, 0), (4, 1), 'King', screen)
test_piece(Knight, paths['Knight'], (1, 7), (2, 5), 'Knight', screen)
test_piece(Rook, paths['Rook'], (0, 0), (0, 1), 'Rook', screen)
test_piece(Queen, paths['Queen'], (3, 0), (3, 3), 'Queen', screen)
test_piece(Pawn, paths['Pawn'], (1, 6), (1, 4), 'Pawn', screen)
# pygame.display.flip()
time.sleep(3)
