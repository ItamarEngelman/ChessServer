import pygame
import os
from constants import *
import requests
from io import BytesIO
from constants import *  # Assuming constants like WIDTH, HEIGHT, etc., are defined in a separate module


class ChessGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('Two-Player Pygame Chess!')
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        self.download_images()
        self.turn_step = 0
        self.selection = 100
        self.valid_moves = []
        self.white_promotions = ['bishop', 'knight', 'rook', 'queen']
        self.white_moved = [False] * 16
        self.black_promotions = ['bishop', 'knight', 'rook', 'queen']
        self.black_moved = [False] * 16
        self.piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
        self.counter = 0
        self.winner = ''
        self.game_over = False
        self.white_ep = (100, 100)
        self.black_ep = (100, 100)
        self.white_promote = False
        self.black_promote = False
        self.promo_index = 100
        self.check = False
        self.castling_moves = []
        self.white_options = []
        self.black_options = []


    def draw_board(self):
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(self.screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
            pygame.draw.rect(self.screen, 'gray', [0, 800, self.WIDTH, 100])
            pygame.draw.rect(self.screen, 'gold', [0, 800, self.WIDTH, 100], 5)
            pygame.draw.rect(self.screen, 'gold', [800, 0, 200, self.HEIGHT], 5)
            status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                           'Black: Select a Piece to Move!', 'Black: Select a Destination!']
            self.screen.blit(self.big_font.render(status_text[self.turn_step], True, 'black'), (20, 820))
            for i in range(9):
                pygame.draw.line(self.screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(self.screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            self.screen.blit(self.medium_font.render('FORFEIT', True, 'black'), (810, 830))
            if self.white_promote or self.black_promote:
                pygame.draw.rect(self.screen, 'gray', [0, 800, self.WIDTH - 200, 100])
                pygame.draw.rect(self.screen, 'gold', [0, 800, self.WIDTH - 200, 100], 5)
                self.screen.blit(self.big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))

    def draw_pieces(self):
        for i in range(len(white_pieces)):
            index = piece_list.index(white_pieces[i])
            if white_pieces[i] == 'pawn':
                screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
            else:
                screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
            if turn_step < 2:
                if selection == i:
                    pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                     100, 100], 2)
        for i in range(len(black_pieces)):
            index = piece_list.index(black_pieces[i])
            if black_pieces[i] == 'pawn':
                screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
            else:
                screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
            if turn_step >= 2:
                if selection == i:
                    pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                      100, 100], 2)




    def download_images(self):
        self.black_queen = pygame.image.load('../assets/images/black queen.png')
        self.black_queen = pygame.transform.scale(self.black_queen, (80, 80))
        self.black_queen_small = pygame.transform.scale(self.black_queen, (45, 45))  # Corrected
        self.black_king = pygame.image.load('../assets/images/black king.png')
        self.black_king = pygame.transform.scale(self.black_king, (80, 80))
        self.black_king_small = pygame.transform.scale(self.black_king, (45, 45))
        self.black_rook = pygame.image.load('../assets/images/black rook.png')
        self.black_rook = pygame.transform.scale(self.black_rook, (80, 80))
        self.black_rook_small = pygame.transform.scale(self.black_rook, (45, 45))
        self.black_bishop = pygame.image.load('../assets/images/black bishop.png')
        self.black_bishop = pygame.transform.scale(self.black_bishop, (80, 80))
        self.black_bishop_small = pygame.transform.scale(self.black_bishop, (45, 45))
        self.black_knight = pygame.image.load('../assets/images/black knight.png')
        self.black_knight = pygame.transform.scale(self.black_knight, (80, 80))
        self.black_knight_small = pygame.transform.scale(self.black_knight, (45, 45))
        self.black_pawn = pygame.image.load('../assets/images/black pawn.png')
        self.black_pawn = pygame.transform.scale(self.black_pawn, (65, 65))
        self.black_pawn_small = pygame.transform.scale(self.black_pawn, (45, 45))
        self.white_queen = pygame.image.load('../assets/images/white queen.png')
        self.white_queen = pygame.transform.scale(self.white_queen, (80, 80))
        self.white_queen_small = pygame.transform.scale(self.white_queen, (45, 45))
        self.white_king = pygame.image.load('../assets/images/white king.png')
        self.white_king = pygame.transform.scale(self.white_king, (80, 80))
        self.white_king_small = pygame.transform.scale(self.white_king, (45, 45))
        self.white_rook = pygame.image.load('../assets/images/white rook.png')
        self.white_rook = pygame.transform.scale(self.white_rook, (80, 80))
        self.white_rook_small = pygame.transform.scale(self.white_rook, (45, 45))
        self.white_bishop = pygame.image.load('../assets/images/white bishop.png')
        self.white_bishop = pygame.transform.scale(self.white_bishop, (80, 80))
        self.white_bishop_small = pygame.transform.scale(self.white_bishop, (45, 45))
        self.white_knight = pygame.image.load('../assets/images/white knight.png')
        self.white_knight = pygame.transform.scale(self.white_knight, (80, 80))
        self.white_knight_small = pygame.transform.scale(self.white_knight, (45, 45))
        self.white_pawn = pygame.image.load('../assets/images/white pawn.png')
        self.white_pawn = pygame.transform.scale(self.white_pawn, (65, 65))
        self.white_pawn_small = pygame.transform.scale(self.white_pawn, (45, 45))
        self.white_images = [self.white_pawn, self.white_queen, self.white_king, self.white_knight, self.white_rook,
                             self.white_bishop]
        self.small_white_images = [pygame.transform.scale(image, (45, 45)) for image in self.white_images]
        self.black_images = [self.black_pawn, self.black_queen, self.black_king, self.black_knight, self.black_rook,
                             self.black_bishop]
        self.small_black_images = [pygame.transform.scale(image, (45, 45)) for image in self.black_images]

    def check_options(self, pieces, locations, turn):
        global castling_moves
        moves_list = []
        all_moves_list = []
        castling_moves = []
        for i in range((len(pieces))):
            location = locations[i]
            piece = pieces[i]
            if piece == 'pawn':
                moves_list = self.check_pawn(location, turn)
            elif piece == 'rook':
                moves_list = self.check_rook(location, turn)
            elif piece == 'knight':
                moves_list = self.check_knight(location, turn)
            elif piece == 'bishop':
                moves_list = self.check_bishop(location, turn)
            elif piece == 'queen':
                moves_list = self.check_queen(location, turn)
            elif piece == 'king':
                moves_list, castling_moves = self.check_king(location, turn)
            all_moves_list.append(moves_list)
        return all_moves_list

    def check_king(self, position, color):
        moves_list = []
        castle_moves = self.check_castling()
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        # 8 squares to check for kings, they can go one square any direction
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list, castle_moves



    def check_bishop(self, position, color):
        moves_list = []
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        for i in range(4):  # up-right, up-left, down-right, down-left
            path = True
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

    def check_rook(self, position, color):
        moves_list = []
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        for i in range(4):  # down, up, right, left
            path = True
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list
    def check_queen(self, position, color):
        moves_list = self.check_bishop(position, color)
        second_list = self.check_rook(position, color)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list
    """
    def load_pieces(self):
        pieces = {}
        for piece_name in PIECES:
            image_url = f"https://example.com/{piece_name}.png"  # Replace with actual URL
            pieces[piece_name] = self.download_image(image_url)
        return pieces
    """

    def check_pawn(position, color):
        moves_list = []
        if color == 'white':
            if (position[0], position[1] + 1) not in white_locations and \
                    (position[0], position[1] + 1) not in black_locations and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
                # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
                if (position[0], position[1] + 2) not in white_locations and \
                        (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                    moves_list.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] - 1, position[1] + 1))
            # add en passant move checker
            if (position[0] + 1, position[1] + 1) == black_ep:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) == black_ep:
                moves_list.append((position[0] - 1, position[1] + 1))
        else:
            if (position[0], position[1] - 1) not in white_locations and \
                    (position[0], position[1] - 1) not in black_locations and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
                # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
                if (position[0], position[1] - 2) not in white_locations and \
                        (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                    moves_list.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
            # add en passant move checker
            if (position[0] + 1, position[1] - 1) == white_ep:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) == white_ep:
                moves_list.append((position[0] - 1, position[1] - 1))
        return moves_list

    def check_knight(position, color):
        moves_list = []
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        # 8 squares to check for knights, they can go two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    # check for valid moves for just selected piece
    def check_valid_moves(self):
        if self.turn_step < 2:
            options_list = self.white_options
        else:
            options_list = self.black_options
        valid_options = options_list[selection]
        return valid_options

    def draw_valid(self, moves):
        if self.turn_step < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(self.screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

    # draw captured pieces on side of screen
    def draw_captured(self):
        for i in range(len(self.captured_pieces_white)):
            captured_piece = self.captured_pieces_white[i]
            index = self.piece_list.index(captured_piece)
            self.screen.blit(self.small_black_images[index], (825, 5 + 50 * i))
        for i in range(len(self.captured_pieces_black)):
            captured_piece = self.captured_pieces_black[i]
            index = self.piece_list.index(captured_piece)
            self.screen.blit(self.small_white_images[index], (925, 5 + 50 * i))

    # draw a flashing square around king if in check
    def draw_check(self):
        self.check = False
        if self.turn_step < 2:
            if 'king' in self.white_pieces:
                king_index = self.white_pieces.index('king')
                king_location = self.white_locations[king_index]
                for i in range(len(self.black_options)):
                    if king_location in self.black_options[i]:
                        self.check = True
                        if self.counter < 15:
                            pygame.draw.rect(self.screen, 'dark red', [self.white_locations[king_index][0] * 100 + 1,
                                                                       self.white_locations[king_index][1] * 100 + 1,
                                                                       100,
                                                                       100], 5)
        else:
            if 'king' in self.black_pieces:
                king_index = self.black_pieces.index('king')
                king_location = self.black_locations[king_index]
                for i in range(len(white_options)):
                    if king_location in white_options[i]:
                        self.check = True
                        if self.counter < 15:
                            pygame.draw.rect(self.screen, 'dark blue', [self.black_locations[king_index][0] * 100 + 1,
                                                                        self.black_locations[king_index][1] * 100 + 1,
                                                                        100,
                                                                        100], 5)

    def draw_game_over(self):
        pygame.draw.rect(self.screen, 'black', [200, 200, 400, 70])
        self.screen.blit(self.font.render(f'{self.winner} won the game!', True, 'white'), (210, 210))
        self.screen.blit(self.font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

    # check en passant because people on the internet won't stop bugging me for it
    def check_ep(self, old_coords, new_coords):
        if self.turn_step <= 1:
            index = self.white_locations.index(old_coords)
            ep_coords = (new_coords[0], new_coords[1] - 1)
            piece = self.white_pieces[index]
        else:
            index = self.black_locations.index(old_coords)
            ep_coords = (new_coords[0], new_coords[1] + 1)
            piece = self.black_pieces[index]
        if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
            # if piece was pawn and moved two spaces, return EP coords as defined above
            pass
        else:
            ep_coords = (100, 100)
        return ep_coords

    # add castling
    def check_castling(self):
        # king must not currently be in check, neither the rook nor king has moved previously, nothing between
        # and the king does not pass through or finish on an attacked piece
        castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
        rook_indexes = []
        rook_locations = []
        king_index = 0
        king_pos = (0, 0)
        if self.turn_step > 1:
            for i in range(len(self.white_pieces)):
                if self.white_pieces[i] == 'rook':
                    rook_indexes.append(self.white_moved[i])
                    rook_locations.append(self.white_locations[i])
                if self.white_pieces[i] == 'king':
                    king_index = i
                    king_pos = self.white_locations[i]
            if not self.white_moved[king_index] and False in rook_indexes and not self.check:
                for i in range(len(rook_indexes)):
                    castle = True
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                         (king_pos[0] + 3, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                    for j in range(len(empty_squares)):
                        if empty_squares[j] in self.white_locations or empty_squares[j] in self.black_locations or \
                                empty_squares[j] in self.black_options or rook_indexes[i]:
                            castle = False
                    if castle:
                        castle_moves.append((empty_squares[1], empty_squares[0]))
        else:
            for i in range(len(self.black_pieces)):
                if self.black_pieces[i] == 'rook':
                    rook_indexes.append(self.black_moved[i])
                    rook_locations.append(self.black_locations[i])
                if self.black_pieces[i] == 'king':
                    king_index = i
                    king_pos = self.black_locations[i]
            if not self.black_moved[king_index] and False in rook_indexes and not self.check:
                for i in range(len(rook_indexes)):
                    castle = True
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                         (king_pos[0] + 3, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                    for j in range(len(empty_squares)):
                        if empty_squares[j] in self.white_locations or empty_squares[j] in self.black_locations or \
                                empty_squares[j] in self.white_options or rook_indexes[i]:
                            castle = False
                    if castle:
                        castle_moves.append((empty_squares[1], empty_squares[0]))
        return castle_moves

    def draw_castling(self, moves):
        if self.turn_step < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(self.screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
            self.screen.blit(self.font.render('king', True, 'black'),
                             (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70))
            pygame.draw.circle(self.screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
            self.screen.blit(self.font.render('rook', True, 'black'),
                             (moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
            pygame.draw.line(self.screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),
                             (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)

    # add pawn promotion
    def check_promotion(self):
        pawn_indexes = []
        white_promotion = False
        black_promotion = False
        promote_index = 100
        for i in range(len(self.white_pieces)):
            if self.white_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if self.white_locations[pawn_indexes[i]][1] == 7:
                white_promotion = True
                promote_index = pawn_indexes[i]
        pawn_indexes = []
        for i in range(len(self.black_pieces)):
            if self.black_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if self.black_locations[pawn_indexes[i]][1] == 0:
                black_promotion = True
                promote_index = pawn_indexes[i]
        return white_promotion, black_promotion, promote_index

    def draw_promotion(self):
        pygame.draw.rect(self.screen, 'dark gray', [800, 0, 200, 420])
        if self.white_promote:
            color = 'white'
            for i in range(len(self.white_promotions)):
                piece = self.white_promotions[i]
                index = self.piece_list.index(piece)
                self.screen.blit(self.white_images[index], (860, 5 + 100 * i))
        elif self.black_promote:
            color = 'black'
            for i in range(len(self.black_promotions)):
                piece = self.black_promotions[i]
                index = self.piece_list.index(piece)
                self.screen.blit(self.black_images[index], (860, 5 + 100 * i))
        pygame.draw.rect(self.screen, color, [800, 0, 200, 420], 8)

    def check_promo_select(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_pos[0] // 100
        y_pos = mouse_pos[1] // 100
        if self.white_promote and left_click and x_pos > 7 and y_pos < 4:
            self.white_pieces[self.promo_index] = self.white_promotions[y_pos]
        elif self.black_promote and left_click and x_pos > 7 and y_pos < 4:
            self.black_pieces[self.promo_index] = self.black_promotions[y_pos]

    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            if self.counter < 30:
                self.counter += 1
            else:
                self.counter = 0
            self.screen.fill('dark gray')
            self.draw_board()
            self.draw_pieces()
            self.draw_captured()
            self.draw_check()
            if not self.game_over:
                white_promote, black_promote, promo_index = self.check_promotion()
                if white_promote or black_promote:
                    self.draw_promotion()
                    self.check_promo_select()
            if self.selection != 100:
                valid_moves = self.check_valid_moves()
                self.draw_valid(valid_moves)
                if self.selected_piece == 'king':
                    self.draw_castling(self.castling_moves)
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100
                    click_coords = (x_coord, y_coord)
                    if self.turn_step <= 1:
                        # Handle white player's turn
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'black'
                        if click_coords in self.white_locations:
                            self.selection = self.white_locations.index(click_coords)
                            self.selected_piece = self.white_pieces[self.selection]
                            if self.turn_step == 0:
                                self.turn_step = 1
                        if click_coords in self.valid_moves and self.selection != 100:
                            white_ep = self.check_ep(self.white_locations[self.selection], click_coords)
                            self.white_locations[self.selection] = click_coords
                            self.white_moved[self.selection] = True
                            if click_coords in self.black_locations:
                                black_piece = self.black_locations.index(click_coords)
                                self.captured_pieces_white.append(self.black_pieces[black_piece])
                                if self.black_pieces[black_piece] == 'king':
                                    self.winner = 'white'
                                self.black_pieces.pop(black_piece)
                                self.black_locations.pop(black_piece)
                                self.black_moved.pop(black_piece)
                            if click_coords == white_ep:
                                black_piece = self.black_locations.index((white_ep[0], white_ep[1] - 1))
                                self.captured_pieces_white.append(self.black_pieces[black_piece])
                                self.black_pieces.pop(black_piece)
                                self.black_locations.pop(black_piece)
                                self.black_moved.pop(black_piece)
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                            self.turn_step = 2
                            self.selection = 100
                            self.valid_moves = []
                        # Add option to castle
                        elif self.selection != 100 and self.selected_piece == 'king':
                            for q in range(len(self.castling_moves)):
                                if click_coords == self.castling_moves[q][0]:
                                    self.white_locations[self.selection] = click_coords
                                    self.white_moved[self.selection] = True
                                    if click_coords == (1, 0):
                                        rook_coords = (0, 0)
                                    else:
                                        rook_coords = (7, 0)
                                    rook_index = self.white_locations.index(rook_coords)
                                    self.white_locations[rook_index] = self.castling_moves[q][1]
                                    self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                                    self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                                    self.turn_step = 2
                                    self.selection = 100
                                    self.valid_moves = []
                    if self.turn_step > 1:
                        # Handle black player's turn
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'white'
                        if click_coords in self.black_locations:
                            self.selection = self.black_locations.index(click_coords)
                            self.selected_piece = self.black_pieces[self.selection]
                            if self.turn_step == 2:
                                self.turn_step = 3
                        if click_coords in self.valid_moves and self.selection != 100:
                            black_ep = self.check_ep(self.black_locations[self.selection], click_coords)
                            self.black_locations[self.selection] = click_coords
                            self.black_moved[self.selection] = True
                            if click_coords in self.white_locations:
                                white_piece = self.white_locations.index(click_coords)
                                self.captured_pieces_black.append(self.white_pieces[white_piece])
                                if self.white_pieces[white_piece] == 'king':
                                    self.winner = 'black'
                                self.white_pieces.pop(white_piece)
                                self.white_locations.pop(white_piece)
                                self.white_moved.pop(white_piece)
                            if click_coords == black_ep:
                                white_piece = self.white_locations.index((black_ep[0], black_ep[1] + 1))
                                self.captured_pieces_black.append(self.white_pieces[white_piece])
                                self.white_pieces.pop(white_piece)
                                self.white_locations.pop(white_piece)
                                self.white_moved.pop(white_piece)
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                            self.turn_step = 0
                            self.selection = 100
                            self.valid_moves = []
                        # Add option to castle
                        elif self.selection != 100 and self.selected_piece == 'king':
                            for q in range(len(self.castling_moves)):
                                if click_coords == self.castling_moves[q][0]:
                                    self.black_locations[self.selection] = click_coords
                                    self.black_moved[self.selection] = True
                                    if click_coords == (1, 7):
                                        rook_coords = (0, 7)
                                    else:
                                        rook_coords = (7, 7)
                                    rook_index = self.black_locations.index(rook_coords)
                                    self.black_locations[rook_index] = self.castling_moves[q][1]
                                    self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                                    self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                                    self.turn_step = 0
                                    self.selection = 100
                                    self.valid_moves = []
                if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_RETURN:
                        # Handle game restart
                        self.game_over = False
                        self.winner = ''
                        self.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        self.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                        self.white_moved = [False] * 16
                        self.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        self.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                        self.black_moved = [False] * 16
                        self.captured_pieces_white = []
                        self.captured_pieces_black = []
                        self.turn_step = 0
                        self.selection = 100
                        self.valid_moves = []
                        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')

            if self.winner != '':
                self.game_over = True
                self.draw_game_over()
            pygame.display.flip()
# Instantiate and run the game
if __name__ == "__main__":
    game = ChessGame()
    game.run_game()
