from constants import *
from Player import *
from utils import *
import pygame

class Game:
    def __init__(self, white_player, black_player):
        self.white_player = white_player
        self.black_player = black_player
        self.turn_count = 0
        self.colors = ["white", "black"]
        self.screen = screen
        self.this_turn_chose = False
        self.this_turn_selected_piece = None
        self.move_taken = False
        self.this_turn_color = colors[self.turn_count % 2]
        self.other_turn_color = colors[(self.turn_count + 1) % 2]
        self.game_over = False
        self.winner = None
    def draw_all_pieces(self):
        self.white_player.draw_pieces(self.screen)
        self.black_player.draw_pieces(self.screen)
    def draw_all_captured_pieces(self):
        self.white_player.draw_captured_pieces(self.screen)
        self.black_player.draw_captured_pieces(self.screen)
    def draw_board(self, this_turn_color):
        """

        :param this_turn_color: a parameter who repessnt whatisthe color of the current turn.
        used to write on the board which turn is playing
        :return: the function that draw to the screen the bard,using gemotry.
        """
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(self.screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
            pygame.draw.rect(self.screen, 'gray', [0, 800, WIDTH, 100])
            pygame.draw.rect(self.screen, 'gold', [0, 800, WIDTH, 100], 5)
            pygame.draw.rect(self.screen, 'gold', [800, 0, 200, HEIGHT], 5)
            status_text = ['White Turn', 'Black Turn']
            if this_turn_color == 'white':
                self.screen.blit(big_font.render(status_text[0], True, 'black'), (20, 820))
            else:
                self.screen.blit(big_font.render(status_text[1], True, 'black'), (20, 820))
            for i in range(9):
                pygame.draw.line(self.screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(self.screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            self.screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
            if Pawn.color_promotion:
                pygame.draw.rect(self.screen, 'gray', [0, 800, WIDTH - 200, 100])
                pygame.draw.rect(self.screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
                self.screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))
    def draw_valid_moves(self, piece):
        """

        :param valid_moves: get valid moves of the selected piece
        :param this_turn_color: the  current color of the turn.
        :return: draw dots in the middle of the squrres in the valid moves given
        """
        if piece.valid_moves != []:
            if piece.type != 'Pawn' and piece.type != 'King':
                valid_moves = piece.valid_moves
                for i in range(len(valid_moves)):
                    pygame.draw.circle(self.screen, (255, 0, 0), (valid_moves[i][0] * 100 + 50, valid_moves[i][1] * 100 + 50), 5)
            else:
                valid_moves = piece.valid_moves[0]
                if valid_moves != []:
                    for i in range(len(valid_moves)):
                        pygame.draw.circle(self.screen, (255, 0, 0), (valid_moves[i][0] * 100 + 50, valid_moves[i][1] * 100 + 50), 5)
                new_valid_moves = piece.valid_moves[1]
                if new_valid_moves != []:
                    if piece.type == 'Pawn':
                        for i in range(len(new_valid_moves)):
                            pygame.draw.circle(self.screen, (255, 0, 0), (new_valid_moves[i][0] * 100 + 50, new_valid_moves[i][1] * 100 + 50), 5)
                    else:
                        for i in range(len(new_valid_moves)):
                            pygame.draw.circle(self.screen, (255, 0, 0),
                                               (new_valid_moves[i][0][0] * 100 + 50, new_valid_moves[i][0][1] * 100 + 50), 5)

    def draw_check(self, this_turn_color):
        """

        :param this_turn_color: the  current color of the turn.
        :return: draw a circle around the king squre. red- if white,and blue if black
        """
        if this_turn_color == 'white' and self.white_player.check:
            king = self.white_player.get_pieces_by_type("King")[0]
            pygame.draw.rect(self.screen, 'dark red', [king.position[0] * 100 + 1,
                                                            king.position[1] * 100 + 1, 100, 100], 5)
        elif this_turn_color == 'black' and self.black_player.check:
            king = self.black_player.get_pieces_by_type("King")[0]
            pygame.draw.rect(self.screen, 'dark blue', [king.position[0] * 100 + 1,
                                                        king.position[1] * 100 + 1, 100, 100], 5)

    def draw_game_over(self):
        """

        :param winner: get the color of the winner player.
        :return: draw a winner measaege
        """
        pygame.draw.rect(self.screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'{self.winner} won the game!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

    def draw_promotion(self):
        """

        :return: draw the promotion options of  the player premoting. using lists from the constans file
        """
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

        :param mouse_cords: the cords of the mouse
        :return: if the mouse click the promotion options with the left button, return which type of piece was selected
        """
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_cords[0] // 100
        y_pos = mouse_cords[1] // 100
        if Pawn.color_promotion == 'white' and left_click and x_pos > 7 and y_pos < 4:
            return white_promotions[y_pos]
        elif Pawn.color_promotion == 'black' and left_click and x_pos > 7 and y_pos < 4:
            return black_promotions[y_pos]
    def draw_turn(self,this_turn_color): # לקחתי את פעולות הציור מתוך הפונקציה - ישתמש בהם על מנת לצייר
        self.draw_board(this_turn_color)
        self.draw_all_pieces()
        self.draw_all_captured_pieces()
        self.draw_check(this_turn_color)
    def execute_regular_move(self, click_coords, this_turn_player, other_turn_player, speacil_piece):
        """
        a  function used in the excute_move function - was seperatedform the main code for convidient.
        :param click_coords: the cords  of the mouse click
        :param this_turn_player: a player  object of the player currently playing the turn
        :param other_turn_player: a player object of the rival player of the player currently playing the turn
        :param speacil_piece: true if the self.this_turn_selected_piece is king or pawn and false if not.
        is needed beacise the structure of the valid moves of pawn and king is diffrent from the rest pf the pieces.
        :return: the first parameter returning is if the game is over and the seacnd is the winnercolor(if no one wen,
        then return None). Also, change the self.move_taken parameter of the game class.
        """
        if not self.move_taken:
            if not speacil_piece and not self.move_taken:
                if click_coords in self.this_turn_selected_piece.valid_moves:
                    self.this_turn_selected_piece.update_position(click_coords)
                    self.this_turn_selected_piece.update_moved()
                    if click_coords in other_turn_player.get_all_positions():
                        captured_piece = other_turn_player.get_piece_by_position(click_coords)
                        this_turn_player.add_captured_piece(captured_piece)
                        other_turn_player.remove_piece(captured_piece)
                    self.move_taken = True
            else:
                if click_coords in self.this_turn_selected_piece.valid_moves[0]:
                    self.this_turn_selected_piece.update_position(click_coords)
                    self.this_turn_selected_piece.update_moved()
                    if click_coords in other_turn_player.get_all_positions():
                        captured_piece = other_turn_player.get_piece_by_position(click_coords)
                        this_turn_player.add_captured_piece(captured_piece)
                        other_turn_player.remove_piece(captured_piece)
                    self.move_taken = True

    def execute_move(self, click_coords, this_turn_player, other_turn_player):
        """

        :param click_coords: the cords of the mouse's click, which should be deliver from the run_game function.
        :param this_turn_player: the player which  hold the current turn
        :param other_turn_player: the rival of the player which  hold the current turn
        :return: nothing, only change parametrs of  the class.
        """
        if Pawn.color_promotion == ('white' or 'black'):  # in order to make sure that the turn that promotion give
            # will be use to promote and not to make other moves
            self.execute_promotion(click_coords, this_turn_player)
        else:
            if click_coords in this_turn_player.get_all_positions():
                self.chose_piece(click_coords, this_turn_player, other_turn_player)
            elif not self.this_turn_selected_piece.type == 'Pawn' and not self.this_turn_selected_piece.type == 'King' and not self.move_taken:
                self.execute_regular_move(click_coords, this_turn_player, other_turn_player, False)
            else:
                self.execute_regular_move(click_coords, this_turn_player, other_turn_player, True)
                self.execute_promotion(click_coords, this_turn_player)
                self.execute_en_passant(click_coords, this_turn_player, other_turn_player)
                self.execute_castling(click_coords, this_turn_player)

    def execute_promotion(self, click_coords, this_turn_player):
        if self.this_turn_selected_piece.type == 'Pawn' and self.this_turn_selected_piece.check_promotion():
            if click_coords[0] == 8 and click_coords[1] < 4:
                new_type = get_key_by_value(dict_of_promotions, click_coords)
                this_turn_player.add_piece(self.this_turn_selected_piece.promotion(new_type))
                this_turn_player.remove_piece(self.this_turn_selected_piece)
                self.move_taken = True
            else:
                self.move_taken = False
    def execute_castling(self, click_coords, this_turn_player):
        if self.this_turn_selected_piece.type == "King" and not self.move_taken:
            print(f"identifing piece type as king ")
            for move in self.this_turn_selected_piece.valid_moves[1]:
                # Check if the clicked coordinates match the move's start position
                print(f"cheacking castlling move : {move}")
                if click_coords == move[0]:
                    print(f"mach founded !, click_coords  = move[0]: {move[0]}")
                    # Update the selected piece's position
                    self.this_turn_selected_piece.update_position(move[0])
                    self.this_turn_selected_piece.update_moved()
                    # Determine board offset based on player color
                    if this_turn_player.color == 'white':
                        off_set = 0
                    else:
                        off_set = 7
                    # Check specific moves to handle castling
                    if move[1] == (2, off_set):
                        # Move the rook involved in 'king-side' castling
                        rook = this_turn_player.get_piece_by_position((0, off_set))
                        rook.update_position((2, off_set))  # Position after castling
                        rook.update_moved()

                    else:
                        # Move the rook involved in 'queen-side' castling
                        rook = this_turn_player.get_piece_by_position((7, off_set))
                        rook.update_position((5, off_set))  # Position after castling
                        rook.update_moved()
                    self.move_taken = True
                    # Exit the loop after handling the move
                    break
    def execute_en_passant(self, click_coords, this_turn_player, other_turn_player):
        if self.this_turn_selected_piece.type == "Pawn" and click_coords in self.this_turn_selected_piece.valid_moves[1] \
                and not self.move_taken:
            print(f"excute en_passon{click_coords}")
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
    def chose_piece(self, click_coords, this_turn_player, other_turn_player):
        """

        :param click_coords: the cords that were clicked
        :param this_turn_player: a player object which represent the player of the current turn
        :return: if the click is in this_turn_player positions , so it change the this_turn_chose to true and
        this_turn_selected_piece to the piece in the  position clicked
        """
        # פעולה שמקבלת משתנים ומחזירה אם ואת הפיסה שנלקחה
        for position in this_turn_player.get_all_positions():
            if click_coords == position:
                self.this_turn_chose, self.this_turn_selected_piece = True, this_turn_player.get_piece_by_position(position)
                self.this_turn_selected_piece.update_valid_moves(this_turn_player, other_turn_player)
    def reset_game_state(self):
        """
        a function that reset  the game status as a  whole.  it goes over all the relevent paramters and inital all of
        them to thier intiall status.
        :return:
        """
        self.white_player = self.white_player.initialize_player()
        self.black_player = self.black_player.initialize_player()
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
        a function which reset the turn. for pawns it updates the since_moved parameter and also update
        the valid moves of the selected piece after he moves. importenet ! beacuse we want that the when we search for
        the enemy_valid_moves (when we change turns), the valid moves will be updated.
        :return:
        """
        self.this_turn_selected_piece.update_valid_moves(this_turn_player, other_turn_player)
        self.move_taken = False
        self.this_turn_chose = False
        self.turn_count = self.turn_count + 1
        self.this_turn_color = self.colors[self.turn_count % 2]
        self.other_turn_color = self.colors[(self.turn_count + 1) % 2]
        Pawn.color_promotion = None
        pawns = this_turn_player.get_pieces_by_type("Pawn")
        for pawn in pawns:
            if pawn != self.this_turn_selected_piece:
                pawn.update_since_moved()
        self.this_turn_selected_piece = None


    def run_game(self):
        run = True
        print("Game started")
        while run:
            timer.tick(fps)  # Controlling the frame rate
            self.screen.fill('dark gray')  # Clearing the screen with a dark gray color
            self.draw_turn(self.this_turn_color)  # Drawing the current turn's game state
            if Pawn.color_promotion == 'white' or Pawn.color_promotion == 'black':
                self.draw_promotion()  # draw the promotion part on the screen
            if self.this_turn_selected_piece:
                self.draw_valid_moves(self.this_turn_selected_piece)
            # Listen for events (like clicks and keyboard inputs)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the close button is clicked
                    run = False
                    print("Quit event detected, closing game")
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                    x_coord, y_coord = event.pos[0] // 100, event.pos[1] // 100
                    click_coords = (x_coord, y_coord)
                    # Check for a forfeit condition based on specific click coordinates
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        self.winner = self.other_turn_color
                        self.game_over = True
                        print(f"Game over by forfeit. Winner: {self.winner}")

                    # Assign players based on the current turn's color
                    if self.this_turn_color == 'white':
                        this_turn_player = self.white_player
                        other_turn_player = self.black_player
                    else:
                        this_turn_player = self.black_player
                        other_turn_player = self.white_player
                    this_turn_player.update_check(other_turn_player)  # updating the check function of the this turn player
                    print(f"this_turn_player in check :{this_turn_player.check}")
                    # Choose a piece or execute a move based on whether a piece is already chosen
                    if not self.this_turn_chose:
                        self.chose_piece(click_coords, this_turn_player, other_turn_player)
                        print(f"Piece chosen at {click_coords}")

                    else:
                        self.execute_move(click_coords, this_turn_player, other_turn_player)
                        if self.move_taken:
                            self.reset_turn(this_turn_player, other_turn_player)
                            print("Turn reset after move")

                if event.type == pygame.KEYDOWN and self.game_over:
                    self.reset_game_state()
                    print("Game state reset after game over")

            # Check if there is a winner and handle game over
            if self.winner:
                self.game_over = True
                self.draw_game_over()
                print(f"Drawing game over screen. Winner: {self.winner}")

            pygame.display.flip()  # Update the display with everything that's been drawn

