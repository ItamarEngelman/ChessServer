import time

from constants import *
from Player import *
from utils import *
import pygame

class Game:
    def __init__(self, white_player, black_player, my_color):
        self.white_player = white_player
        self.black_player = black_player
        self.turn_count = 0
        self.colors = ["white", "black"]
        self.screen = screen
        self.this_turn_chose = False
        self.this_turn_selected_piece = None
        self.move_taken = False
        self.this_turn_color = self.colors[self.turn_count % 2]
        self.other_turn_color = self.colors[(self.turn_count + 1) % 2]
        self.game_over = False
        self.winner = None
        self.my_color = my_color
        self.pause = self.my_color != self.this_turn_color
        self.move_type = None
        self.chosen_piece_pos = None
        self.should_quit = False
        self.last_move_to = (100, 100)

    def draw_all_pieces(self):
        """
        Draw all pieces on the board.
        """
        self.white_player.draw_pieces(self.screen)
        self.black_player.draw_pieces(self.screen)

    def draw_all_captured_pieces(self):
        """
        Draw all captured pieces on the side.
        """
        self.white_player.draw_captured_pieces(self.screen)
        self.black_player.draw_captured_pieces(self.screen)

    def draw_board(self):
        """
        Draw the chessboard on the screen without the bottom line indicating the turn.
        """
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(self.screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])

        pygame.draw.rect(self.screen, 'gray', [800, HEIGHT - 100, WIDTH - 800, 100])  # Bottom area for forfeit
        pygame.draw.rect(self.screen, 'black', [800, HEIGHT - 100, WIDTH - 800, 100], 5)  # Thicker black border for forfeit area

        # Draw a line between captured pieces area and the board
        pygame.draw.rect(self.screen, 'black', [800, HEIGHT - 102, WIDTH - 800, 4])  # Adjusted thickness and position

        # Adjusted position for "FORFEIT" text
        self.screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, HEIGHT - 90))

    def draw_valid_moves(self, piece):
        """
        Draw valid moves for the selected piece.

        :param piece: The selected piece.
        :return: Draw dots in the middle of the squares for the valid moves given.
        """
        if piece.valid_moves:
            if piece.type not in ['Pawn', 'King']:
                valid_moves = piece.valid_moves
                for move in valid_moves:
                    pygame.draw.circle(self.screen, (255, 0, 0), (move[0] * 100 + 50, move[1] * 100 + 50), 5)
            else:
                valid_moves = piece.valid_moves[0]
                for move in valid_moves:
                    pygame.draw.circle(self.screen, (255, 0, 0), (move[0] * 100 + 50, move[1] * 100 + 50), 5)
                new_valid_moves = piece.valid_moves[1]
                for move in new_valid_moves:
                    pygame.draw.circle(self.screen, (255, 0, 0), (move[0] * 100 + 50, move[1] * 100 + 50), 5)

    def draw_check(self, this_turn_color):
        """
        Draw a circle around the king's square if in check.

        :param this_turn_color: The current color of the turn.
        :return: Draw a circle around the king square. Red if white, and blue if black.
        """
        if this_turn_color == 'white':
            this_turn_player = self.white_player
        else:
            this_turn_player = self.black_player
        if self.my_color == this_turn_color and this_turn_player.check:
            kings = this_turn_player.get_pieces_by_type("King")
            if kings:
                king = kings[0]
                pygame.draw.rect(self.screen, 'dark red', [king.position[0] * 100 + 1,
                                                           king.position[1] * 100 + 1, 100, 100], 5)

    def draw_game_over(self):
        """
        Draw the game over screen with the winner.
        """
        if self.game_over:
            pygame.draw.rect(self.screen, 'black', [200, 200, 400, 40])
            font = pygame.font.Font(None, 36)  # Ensure you have initialized 'font' correctly
            self.screen.blit(font.render(f'{self.winner} won the game!', True, 'white'), (210, 210))
            print(f"Game over screen drawn: winner={self.winner}")
            pygame.display.flip()  # Update the display to show changes

    def draw_promotion(self):
        """
        Draw the promotion options for the player.

        :return: Draw the promotion options of the player promoting using lists from the constants file.
        """
        if self.my_color == self.this_turn_color:
            color = 'green'  # Default color, change it to something that makes sense in your context
            pygame.draw.rect(self.screen, 'dark gray', [800, 0, 200, 420])
            if Pawn.color_promotion == 'white':
                color = 'white'
                for i in range(len(white_promotions)):
                    piece = white_promotions[i]
                    index = piece_list.index(piece)
                    screen.blit(white_images[index], (860, 5 + 100 * i))
            elif Pawn.color_promotion == 'black':
                color = 'black'
                for i in range(len(black_promotions)):
                    piece = black_promotions[i]
                    index = piece_list.index(piece)
                    screen.blit(black_images[index], (860, 5 + 100 * i))
            pygame.draw.rect(screen, color, [800, 0, 200, 420], 8)

    def check_promo_select(self, mouse_cords):
        """
        Check if a promotion option was selected.

        :param mouse_cords: The coordinates of the mouse.
        :return: If the mouse clicked the promotion options with the left button, return which type of piece was selected.
        """
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_cords[0] // 100
        y_pos = mouse_cords[1] // 100
        if Pawn.color_promotion == 'white' and left_click and x_pos > 7 and y_pos < 4:
            return white_promotions[y_pos]
        elif Pawn.color_promotion == 'black' and left_click and x_pos > 7 and y_pos < 4:
            return black_promotions[y_pos]

    def draw_turn(self, this_turn_color):
        """
        Draw the current state of the game.

        :param this_turn_color: The current color of the turn.
        """
        self.draw_board()
        self.draw_all_pieces()
        self.draw_all_captured_pieces()
        self.draw_check(this_turn_color)

    def draw_other_player_quit(self, this_turn_player, other_turn_player):
        """
        Draw the screen indicating the other player has quit.

        :param this_turn_player: The player currently playing the turn.
        :param other_turn_player: The player who quit.
        """
        pygame.draw.rect(self.screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'{other_turn_player.color} disconnected, {this_turn_player.color} won!', True, 'white'), (210, 210))
        screen.blit(font.render(f'You may close the window', True, 'white'), (210, 240))
        pygame.display.flip()  # Update the display to show changes

    def execute_regular_move(self, click_coords, this_turn_player, other_turn_player, special_piece):
        """
        Execute a regular move for the selected piece.

        :param click_coords: The coordinates of the mouse click.
        :param this_turn_player: The player currently playing the turn.
        :param other_turn_player: The rival player.
        :param special_piece: True if the selected piece is a king or pawn, False otherwise.
        :return: Returns if the game is over and the winner color (if no one won, then return None). Also, change the self.move_taken parameter of the game class.
        """
        if not self.move_taken:
            if not special_piece and not self.move_taken:
                if click_coords in self.this_turn_selected_piece.valid_moves:
                    self.this_turn_selected_piece.update_position(click_coords)
                    self.this_turn_selected_piece.update_moved()
                    if click_coords in other_turn_player.get_all_positions():
                        captured_piece = other_turn_player.get_piece_by_position(click_coords)
                        this_turn_player.add_captured_piece(captured_piece)
                        other_turn_player.remove_piece(captured_piece)
                    self.move_taken = True
                    self.last_move_to = self.this_turn_selected_piece.position
                    self.move_type = "move"
            else:
                if click_coords in self.this_turn_selected_piece.valid_moves[0]:
                    self.this_turn_selected_piece.update_position(click_coords)
                    self.this_turn_selected_piece.update_moved()
                    if click_coords in other_turn_player.get_all_positions():
                        captured_piece = other_turn_player.get_piece_by_position(click_coords)
                        this_turn_player.add_captured_piece(captured_piece)
                        other_turn_player.remove_piece(captured_piece)
                    self.move_taken = True
                    self.last_move_to = self.this_turn_selected_piece.position
                    self.move_type = "move"

    def execute_move(self, click_coords, this_turn_player, other_turn_player):
        """
        Execute a move based on the clicked coordinates.

        :param click_coords: The coordinates of the mouse click.
        :param this_turn_player: The player currently playing the turn.
        :param other_turn_player: The rival player.
        :return: None. Only changes parameters of the class.
        """
        print(f"Executing move: click_coords={click_coords}, this_turn_player={this_turn_player.color}, other_turn_player={other_turn_player.color}")
        if Pawn.color_promotion in ['white', 'black']:
            print("Handling promotion")
            self.execute_promotion(click_coords, this_turn_player)
            self.move_type = 'promotion'
        else:
            if click_coords in this_turn_player.get_all_positions():
                self.chose_piece(click_coords, this_turn_player, other_turn_player)
            elif self.this_turn_selected_piece and self.this_turn_selected_piece.type not in ['Pawn', 'King']:
                self.execute_regular_move(click_coords, this_turn_player, other_turn_player, False)
            else:
                self.execute_regular_move(click_coords, this_turn_player, other_turn_player, True)
                self.execute_promotion(click_coords, this_turn_player)
                self.execute_en_passant(click_coords, this_turn_player, other_turn_player)
                self.execute_castling(click_coords, this_turn_player)
        print(f"Move executed: move_type={self.move_type}, game_over={self.game_over}, winner={self.winner}")

    def execute_promotion(self, click_coords, this_turn_player):
        """
        Execute promotion for a pawn if applicable.

        :param click_coords: The coordinates of the mouse click.
        :param this_turn_player: The player currently playing the turn.
        :return: None. Only changes parameters of the class.
        """
        if self.this_turn_selected_piece.type == 'Pawn' and self.this_turn_selected_piece.check_promotion():
            if click_coords[0] in [8, 9] and click_coords[1] < 4:
                new_type = get_key_by_value(dict_of_promotions, click_coords)
                promoted_piece = self.this_turn_selected_piece.promotion(new_type)
                this_turn_player.add_piece(promoted_piece)
                this_turn_player.remove_piece(self.this_turn_selected_piece)
                self.move_taken = True
                self.last_move_to = click_coords
                self.move_type = "promotion"
            else:
                self.move_taken = False
                self.move_type = "move"
                self.last_move_to = click_coords

    def execute_castling(self, click_coords, this_turn_player):
        """
        Execute castling if applicable.

        :param click_coords: The coordinates of the mouse click.
        :param this_turn_player: The player currently playing the turn.
        :return: None. Only changes parameters of the class.
        """
        if self.this_turn_selected_piece.type == "King" and not self.move_taken:
            for move in self.this_turn_selected_piece.valid_moves[1]:
                if click_coords == move[0]:
                    self.this_turn_selected_piece.update_position(move[0])
                    self.this_turn_selected_piece.update_moved()
                    if this_turn_player.color == 'white':
                        off_set = 0
                    else:
                        off_set = 7
                    if move[1] == (2, off_set):
                        rook = this_turn_player.get_piece_by_position((0, off_set))
                        rook.update_position((2, off_set))
                        rook.update_moved()
                    else:
                        rook = this_turn_player.get_piece_by_position((7, off_set))
                        rook.update_position((5, off_set))
                        rook.update_moved()
                    self.move_taken = True
                    self.last_move_to = self.this_turn_selected_piece.position
                    self.move_type = "move"
                    break

    def execute_en_passant(self, click_coords, this_turn_player, other_turn_player):
        """
        Execute en passant if applicable.

        :param click_coords: The coordinates of the mouse click.
        :param this_turn_player: The player currently playing the turn.
        :param other_turn_player: The rival player.
        :return: None. Only changes parameters of the class.
        """
        if self.this_turn_selected_piece.type == "Pawn" and click_coords in self.this_turn_selected_piece.valid_moves[1] and not self.move_taken:
            print(f"execute_en_passant {click_coords}")
            self.this_turn_selected_piece.update_position(click_coords)
            self.this_turn_selected_piece.update_moved()
            if this_turn_player.color == 'white':
                offset = -1
            else:
                offset = 1
            captured_piece = other_turn_player.get_piece_by_position((click_coords[0], click_coords[1] + offset))
            this_turn_player.add_captured_piece(captured_piece)
            other_turn_player.remove_piece(captured_piece)
            self.move_taken = True
            self.last_move_to = self.this_turn_selected_piece.position
            self.move_type = "move"

    def chose_piece(self, click_coords, this_turn_player, other_turn_player):
        """
        Choose a piece based on the clicked coordinates.

        :param click_coords: The coordinates that were clicked.
        :param this_turn_player: The player object representing the player of the current turn.
        :param other_turn_player: The player object representing the rival player.
        :return: If the click is in this_turn_player positions, set this_turn_chose to True and this_turn_selected_piece to the piece in the clicked position.
        """
        print(f"checking each position if my own player positions")
        for position in this_turn_player.get_all_positions():
            print(f"check {position}")
            if click_coords == position:
                print(f"found position {position}")
                self.this_turn_chose, self.this_turn_selected_piece = True, this_turn_player.get_piece_by_position(position)
                self.this_turn_selected_piece.update_valid_moves(this_turn_player, other_turn_player)
                self.chosen_piece_pos = self.this_turn_selected_piece.position
                break

    def reset_game_state(self):
        """
        Reset the game state to the initial setup.

        :return: None. Only changes parameters of the class.
        """
        self.white_player.initialize_player()
        self.black_player.initialize_player()
        self.turn_count = 0
        self.this_turn_chose = False
        self.this_turn_selected_piece = None
        self.move_taken = False
        self.this_turn_color = self.colors[self.turn_count % 2]
        self.other_turn_color = self.colors[(self.turn_count + 1) % 2]
        self.game_over = False
        self.winner = None

    def reset_turn(self, this_turn_player, other_turn_player):
        """
        Reset the turn state.

        :param this_turn_player: The player object representing the player of the current turn.
        :param other_turn_player: The player object representing the rival player.
        :return: None. Only changes parameters of the class.
        """
        if self.this_turn_selected_piece is not None and self.move_taken:
            self.this_turn_selected_piece.update_valid_moves(this_turn_player, other_turn_player)
        self.move_taken = False
        self.pause = not self.pause
        self.move_type = None
        self.this_turn_chose = False
        self.turn_count += 1
        self.this_turn_color = self.colors[self.turn_count % 2]
        self.other_turn_color = self.colors[(self.turn_count + 1) % 2]
        Pawn.color_promotion = None
        pawns = this_turn_player.get_pieces_by_type("Pawn")
        for pawn in pawns:
            if pawn != self.this_turn_selected_piece:
                pawn.update_since_moved()
        self.this_turn_selected_piece = None

    def draw_stale_mate(self):
        """
        Draw the stalemate screen.

        :return: None. Only changes parameters of the class.
        """
        pygame.draw.rect(self.screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'{self.this_turn_color} in stalemate, it is a tie', True, 'white'), (210, 210))

    def run_game(self):
        """
        Run the main game loop.

        :return: None. Only changes parameters of the class.
        """
        timer.tick(fps)
        self.screen.fill('dark gray')
        self.draw_turn(self.this_turn_color)

        if self.this_turn_selected_piece:
            self.draw_valid_moves(self.this_turn_selected_piece)

        if Pawn.color_promotion in ['white', 'black']:
            self.draw_promotion()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_quit = True
                self.game_over = True
                self.winner == self.other_turn_color
                self.move_type = "quit"
                print("Quit event detected")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.game_over and not self.pause and self.my_color == self.this_turn_color:
                    x_coord, y_coord = event.pos[0] // 100, event.pos[1] // 100
                    click_coords = (x_coord, y_coord)
                    print(f"Mouse click detected at {click_coords}")
                    self.process_click(click_coords)

        pygame.display.flip()

    def process_click(self, click_coords):
        """
        Process the mouse click during the game.

        :param click_coords: The coordinates of the mouse click.
        :return: None. Only changes parameters of the class.
        """
        if self.game_over or self.pause or self.my_color != self.this_turn_color:
            print(f"Ignoring click at {click_coords}: game_over={self.game_over}, pause={self.pause}, my_color={self.my_color}, this_turn_color={self.this_turn_color}")
            return

        this_turn_player = self.white_player if self.this_turn_color == 'white' else self.black_player
        other_turn_player = self.black_player if self.this_turn_color == 'white' else self.white_player
        this_turn_player.update_check(other_turn_player)
        this_turn_player.update_pawns_valid_moves(other_turn_player)

        if click_coords in [(8, 7), (9, 7)]:
            print("Forfeit button clicked")
            self.winner = self.other_turn_color
            self.game_over = True
            self.chosen_piece_pos = (-1, -1)
            self.last_move_to = (-1, -1)
            self.move_taken = True
            self.move_type = self.winner
            return

        if not self.this_turn_chose:
            print(f"First click at {click_coords}, selecting piece")
            self.chose_piece(click_coords, this_turn_player, other_turn_player)
        else:
            print(f"Second click at {click_coords}, executing move")
            self.execute_move(click_coords, this_turn_player, other_turn_player)
            if self.move_taken:
                print(f"Move taken, resetting turn for {this_turn_player.color}")
                self.check_game_status(this_turn_player, other_turn_player)

    def check_game_status(self, this_turn_player, other_turn_player):
        """
        Check the game status to determine if there is a checkmate or stalemate.

        :param this_turn_player: The player currently playing the turn.
        :param other_turn_player: The rival player.
        :return: None. Only changes parameters of the class.
        """
        this_turn_player.update_check(other_turn_player)
        this_turn_player.update_pawns_valid_moves(other_turn_player)
        if this_turn_player.check_stale_mate():
            print("Stalemate detected")
            self.draw_stale_mate()
            self.game_over = True
        if self.game_over:
            self.draw_game_over()
        elif this_turn_player.check:
            if this_turn_player.check_mate(other_turn_player):
                print(f"Checkmate detected, winner is {other_turn_player.color}")
                self.game_over = True
                self.winner = self.other_turn_color
