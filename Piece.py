from constants import *
from utils import  *
from abc import ABC, abstractmethod
import pygame
class Piece():
    color = None
    image_path = ''
    position = (-1, -1)
    type = None
    moved = False
    valid_moves = []
    @abstractmethod
    def update_position(self):
        pass
    @abstractmethod
    def update_moved(self):
        pass

    @abstractmethod
    def update_valid_moves(self):
        pass

    def draw(self, screen):
        """

        :param screen: get a screen to print the image on. pharps will be a class of his own(the screens i mean)

        :return: blit (draws) the image into the screen
        """
        image = pygame.image.load(self.image_path)
        print(image)
        image = pygame.transform.scale(image, (65, 65))
        screen.blit(image, (self.position[0] * 100 + 10, self.position[1] * 100 + 10))

    def capture_drawing(self):
        """
        :return: returns the image of the pawn in the smaller version sutiable  for captured pieces
        """
        image = pygame.transform.scale(pygame.image.load(self.image_path), (45, 45))
        return image

