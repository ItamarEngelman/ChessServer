import pygame
from old_tries.chessgame import  ChessGame # Replace 'your_file_name' with the actual name of your file

def main():
    pygame.init()
    game = ChessGame()
    game.run_game()
    pygame.quit()

if __name__ == "__main__":
    main()