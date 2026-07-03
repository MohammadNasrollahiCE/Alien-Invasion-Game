import pygame
import Settings
import AlienInvasion
import pygame.font

class Button:
    """ a class to build buttons for the game """

    def __init__(self , ai_game , msg):
        """ initialize button attributes """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #set the dimention and properties of the button
        self.width , self.height = 200 , 50
        self.button_color = (0 , 135 , 0)
        self.text_color = (255 , 255 , 255)
        self.font = pygame.font.SysFont(None , 48)

        #build the button's rect object and center it
        self.rect = pygame.Rect(0 , 0 , self.width , self.height)
        self.rect.center = self.screen_rect.center

        #the button message needs to be prepped only once
        self._prepMsg(msg)

    def _prepMsg(self , msg):
        """ turn message into a rendered image and center
            text on the button"""
        self.msg_image = self.font.render(msg , True , self.text_color , self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def drawButton(self):
        """ draw blank button and then draw mwwsage """
        self.screen.fill(self.button_color , self.rect)
        self.screen.blit(self.msg_image , self.msg_image_rect)
        pygame.mouse.set_visible(True)