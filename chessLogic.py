
import pygame
from workingFunctions import *
import time
import sys
import pygame
pygame.init()





def check_valid_moves(color):
    if color == 'white':
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    #print(f"castling_moves : {castling_moves}")
    if color == 'white' and white_pieces[selection] == "king":
        for move in castling_moves:
            valid_options.append(move[0])
    if color == 'black' and black_pieces[selection] == "king":
        for move in castling_moves:
            valid_options.append(move[0])
        valid_options.append(castling_moves)
    #print(f"valid_options : {valid_options}")
    return valid_options



def reset_turn():
    global selection, valid_moves
    selection = 100
    valid_moves = []


def reset_game_state():
    global white_pieces, white_locations, white_moved, black_pieces, black_locations, black_moved, move_taken, game_over, turn_count
    global captured_pieces_white, captured_pieces_black, selection, valid_moves, this_turn_chose, this_turn_selected_piece, winner
    game_over = False
    winner = None
    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    white_moved = [False, False, False, False, False, False, False, False,
                   False, False, False, False, False, False, False, False]
    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    black_moved = [False, False, False, False, False, False, False, False,
                   False, False, False, False, False, False, False, False]
    captured_pieces_white = []
    captured_pieces_black = []
    selection = 100
    valid_moves = []
    this_turn_chose = False
    this_turn_selected_piece = None
    move_taken = False
    turn_count = 0

def debug_game_state():
    # Print current state before reset
    print("Game Over:", game_over)
    print("Winner:", winner)
    print("White Pieces:", white_pieces)
    print("White Locations:", white_locations)
    print("White Moved:", white_moved)
    print("Black Pieces:", black_pieces)
    print("Black Locations:", black_locations)
    print("Black Moved:", black_moved)
    print("Captured Pieces White:", captured_pieces_white)
    print("Captured Pieces Black:", captured_pieces_black)
    print("Selection:", selection)
    print("Valid Moves:", valid_moves)


def execute_move(click_coords, valid_moves, this_turn_color, other_turn_color, this_turn_locations, other_turn_locations, this_turn_moves, other_turn_moves, this_turn_captured_pieces,
             other_turn_pieces, this_turn_pieces, this_turn_selected_piece):
    global selection, this_turn_chose
    if click_coords in this_turn_locations:
        this_turn_chose, this_turn_selected_piece = chose_piece(click_coords, this_turn_color, this_turn_locations, this_turn_pieces)
        execute_castling(click_coords, this_turn_locations, this_turn_moves, this_turn_color, this_turn_selected_piece)
    elif click_coords in valid_moves and selection != 100:
        this_turn_ep = check_ep(this_turn_color, this_turn_locations[selection], click_coords)
        other_turn_ep = check_ep(other_turn_color, other_turn_locations[selection], click_coords)
        this_turn_locations[selection] = click_coords
        this_turn_moves[selection] = True
        if click_coords in other_turn_locations:
            other_turn_piece_index = other_turn_locations.index(click_coords) # לוקח את האינדקס עצמו של החתיכה, שאיתה נוכל למצוא בשאר הרשימות את הפרטים הרלוונטים. אבל כרדע מדובר ברק מספר יחיד
            this_turn_captured_pieces.append(other_turn_pieces[other_turn_piece_index])
            if other_turn_pieces[other_turn_piece_index] == 'king':
                return True, this_turn_color, True
            remove_piece(other_turn_piece_index, other_turn_pieces, other_turn_locations, other_turn_moves)
        if click_coords == other_turn_ep:
            if this_turn_color == "white":
                offset = -1
            else:
                offset = 1
            target_coord = (other_turn_ep[0], other_turn_ep[1] + offset)
            other_turn_piece_index = other_turn_locations.index(target_coord)
            this_turn_captured_pieces.append(other_turn_pieces[other_turn_piece_index])
            remove_piece(other_turn_piece_index, other_turn_pieces, other_turn_locations, other_turn_moves)
        execute_castling(click_coords, this_turn_locations, this_turn_moves, this_turn_color, this_turn_selected_piece)
        reset_turn()
        return False, None, True# הראשון זה האם המשחק נגמר,השני זה המנצח, השלישי אם מהלך יתרחש
    return False, None, False

def execute_castling(click_coords, this_turn_locations, this_turn_moves, this_turn_color,this_turn_selected_piece):

    print(f"Debug: Clicked coordinates: {click_coords}\n")
    print(f"Debug: Currently selected piece: {this_turn_selected_piece}\n")
    print(f"selection in  execute_castling: {selection}")
    if selection != 100 and this_turn_selected_piece == 'king':
        print("in the execute_castling main if")
        for q, move in enumerate(castling_moves):
            #print(f"Debug: Checking castling move {move} at index {q}")
            if click_coords == move[0]:
                #print(f"Debug: Match found with clicked coordinates at {click_coords}")
                this_turn_locations[selection] = click_coords
                this_turn_moves[selection] = True
                if this_turn_color == 'white':
                    if click_coords == (1, 0):
                        rook_coords = (0, 0)
                    else:
                        rook_coords = (7, 0)
                elif this_turn_color == 'black':
                    if click_coords == (1, 7):
                        rook_coords = (0, 7)
                    else:
                        rook_coords = (7, 7)

                print(f"Debug: Rook coordinates set to {rook_coords} for moving rook")
                rook_index = this_turn_locations.index(rook_coords)
                this_turn_locations[rook_index] = move[1]
                print(f"Debug: Rook moved from {rook_coords} to {move[1]}")
                reset_turn()
                print("Debug: Turn reset after castling")
                return False, None, True

    print("Debug: No valid castling executed")
    return False, None, None



def chose_piece(click_coords, this_turn_color, this_turn_locations, this_turn_pieces):
    #פעולה שמקבלת משתנים ומחזירה אם ואת הפיסה שנלקחה
    global selection, valid_moves
    update_options(this_turn_color)
    if click_coords in this_turn_locations:
        selection = this_turn_locations.index(click_coords)
        this_turn_selected_piece = this_turn_pieces[selection]
    if selection != 100:
        valid_moves = check_valid_moves(this_turn_color)
        return True, this_turn_selected_piece
    return False, None


def update_options(color):
    if color == 'white':
        global white_options
        white_options, castling_moves = check_options(white_pieces, white_locations, 'white')
    else:
        global black_options
        black_options, castling_moves = check_options(black_pieces, black_locations, 'black')


def draw_turn(this_turn_color): # לקחתי את פעולות הציור מתוך הפונקציה - ישתמש בהם על מנת לצייר
    draw_board(this_turn_color)
    draw_pieces(this_turn_color)
    draw_captured()
    draw_check(this_turn_color)

black_options, castling_moves = check_options(black_pieces, black_locations, 'black')
white_options, castling_moves = check_options(white_pieces, white_locations, 'white')
run = True

turn_count = int(sys.argv[1])  # משהו של אורי
turn_count = 0  # Initialize turn_count outside the main loop

this_turn_chose = False
this_turn_selected_piece = None
move_taken = False


while run:
    # Update the colors for each turn dynamically inside the loop
    this_turn_color = colors[turn_count % 2]
    other_turn_color = colors[(turn_count + 1) % 2]

    timer.tick(fps)
    counter = (counter + 1) % 30  # Increment and reset counter every 30 frames

    # Clear and redraw the board and pieces
    screen.fill('dark gray')
    draw_turn(this_turn_color)

    # Handle game-over scenarios and potential restarts
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()

        # Update valid moves based on the current state and selection
        if selection != 100:
            valid_moves = check_valid_moves(this_turn_color)
            draw_valid(valid_moves, this_turn_color)

    # listen to the server for the other player turn
    # STOP and listen



    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord, y_coord = event.pos[0] // 100, event.pos[1] // 100
            click_coords = (x_coord, y_coord)

            # If a player forfeits, the other player wins
            if click_coords == (8, 8) or click_coords == (9, 8): # לטפל בהודעת הכניעה
                winner = other_turn_color
                game_over = True

            # Define game entities based on turn color dynamically
            if this_turn_color == 'white':
                this_turn_locations = white_locations
                other_turn_locations = black_locations
                this_turn_moves = white_moved
                other_turn_moves = black_moved
                this_turn_captured_pieces = captured_pieces_white
                other_turn_captured_pieces = captured_pieces_black
                this_turn_pieces = white_pieces
                other_turn_pieces = black_pieces
            else:
                this_turn_locations = black_locations
                other_turn_locations = white_locations
                this_turn_moves = black_moved
                other_turn_moves = white_moved
                this_turn_captured_pieces = captured_pieces_black
                other_turn_captured_pieces = captured_pieces_white
                this_turn_pieces = black_pieces
                other_turn_pieces = white_pieces

            # Logic to handle piece selection and moves
            if this_turn_chose == False:
                this_turn_chose, this_turn_selected_piece = chose_piece(click_coords, this_turn_color, this_turn_locations, this_turn_pieces)
            else:
                game_over, winner, move_taken = execute_move(click_coords, valid_moves, this_turn_color, other_turn_color, this_turn_locations, other_turn_locations, this_turn_moves, other_turn_moves, this_turn_captured_pieces, other_turn_pieces, this_turn_pieces, this_turn_selected_piece)
                if move_taken:
                    turn_count += 1
                    this_turn_chose = False
                    this_turn_selected_piece = None  # Increment the turn counter after each full turn
                    reset_turn()
            #debug_game_state()
            draw_turn(this_turn_color)
        if event.type == pygame.KEYDOWN and game_over:
            reset_game_state()
    if winner:
        game_over = True
        draw_game_over(winner)

    pygame.display.flip()

pygame.quit()







