import pygame
import Serrings
import AlienInvasion

class Ship:
    """ a class to manage the ship """

    def __init__(self , ai_game):
        """initialize the ship and set its starting position """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #load the ship image and get its rect
        self.image = pygame.image.load("ship1.jpg")
        self.rect = self.image.get_rect()

        #starting each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a float for the ship's exact horizental position
        self.x = float(self.rect.x)

        #movement flag , start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False
        
    def updateShip(self):
        """ update the ship's position based on the movement flag """
        #update the ship's x value , not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #update rect object from self.x
        self.rect.x = self.x

    def blitMe(self):
        """ draw a ship at its current location"""
        self.screen.blit(self.image , self.rect)

    def centerShip(self):
        """ center the ship on the screen """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)