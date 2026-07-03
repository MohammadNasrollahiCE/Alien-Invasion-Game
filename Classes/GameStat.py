import pygame
from Classes import Settings
import AlineInvasion

class GameState:
    """ track statitics for Alien Invasion """
    def __init__(self , ai_game):
        self.settings = ai_game.settings
        self.resetStats()

    def resetStats(self):
        """ initialize statistics that can change during the game """
        self.ship_left = self.settings.ship_limit