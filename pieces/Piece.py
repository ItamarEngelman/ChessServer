from utils import *
from abc import ABC, abstractmethod
import pygame
from abc import ABC, abstractmethod

class Piece(ABC):  # מחלקה אבסטרקטית

    def __init__(self, color, position, image_path):
        self.color = color
        self.position = position
        self.image_path = image_path
        self.moved = False
        self.type = None
        self.valid_moves = []

    def update_position(self, new_position):
        """

        :param new_position: the new position of the piece
        :return: void, just change the piece position
        """
        self.position = new_position
    def update_moved(self):
        """

        :return: change the piece "moved" parameter to true
        """
        self.moved = True
    @abstractmethod
    def update_valid_moves(self, my_player, enemy_player):
        pass

    def draw(self, screen, piece_size=(65, 65), piece_position_offset=(10, 10)):
        """
        :param screen: get a screen to print the image on.
        :param piece_size: size of the piece (width, height)
        :param piece_position_offset: offset for piece position (x, y)
        :return: blit (draws) the image into the screen
        """
        image = pygame.image.load(self.image_path)
        image = pygame.transform.scale(image, piece_size)
        screen.blit(image, (
        self.position[0] * 100 + piece_position_offset[0], self.position[1] * 100 + piece_position_offset[1]))

    def capture_drawing(self):
        """
        Return the image of the pawn in a smaller version suitable for captured pieces.
        """
        image = pygame.transform.scale(pygame.image.load(self.image_path), (35, 35))  # Adjusted size
        return image

