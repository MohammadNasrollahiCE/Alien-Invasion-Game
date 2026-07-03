class Settings:
    """ a class for store all setting for alien invasion """

    def __init__(self):
        """ initialize the game settings """
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230 , 230 , 230)
        #ship settings
        self.ship_speed = 3.0
        self.ship_limit = 3
        #bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60 , 60 , 60)
        self.bullet_allowed = 5
        #alien settings
        self.alien_speed = 3.0
        self.fleet_drop_speed = 30
        #fleet_direction of 1 represent right, -1 represent left
        self.fleet_direction = 1