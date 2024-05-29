import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
# game variables and images
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']

black_promotions = ['bishop', 'knight', 'rook', 'queen']

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
dict_of_promotions = {"Bishop": (8, 0), "Knight": (8, 1), "Rook": (8, 2), "Queen": (8, 3)}