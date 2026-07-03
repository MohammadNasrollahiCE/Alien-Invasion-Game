import pygame
import sys
from time import sleep

print("start")

from Classes.Settings import Settings
from Classes.Ship import Ship
from Classes.Alien import Alien
from Classes.GameStat import GameState
from Classes.Button import Button
from Classes.Bullet import Bullet

class AlienInvasion:
    """ overal class to manage game assets and behavior """
    def __init__(self):
        """initialize the game and create the game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        """create a screen"""
        self.screen = pygame.display.set_mode((0 , 0) , pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invaion")

        #create an instance to store game statistics
        self.stats = GameState(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._createFleet()

        #set the background color
        self.bg_color = (230 , 230 , 230)

        #start Alien Invation in an inactive state
        self.game_active = False

        #make the play button
        self.play_button = Button(self , "Play")

    def _createFleet(self):
        """ create the fleet of aliens """
        #make an alien and keep adding aliens to until there's no room lwft
        #spacing between aliens is one alien width and one alien heght
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size

        current_x , current_y = alien_width , alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x , current_y)    
                current_x += 2 * alien_width
            
            #finished a row , reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self , x_position , y_position):
        """ create an alien and place it in the fleet """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _changeFleetDirection(self):
        """ drop the entrie fleet and change the fleets' direction  """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _checkFleetEdges(self):
        """ respond appropriately if any aliens have reached an edge """
        for alien in self.aliens.sprites():
            if alien.checkEdge():
                self._changeFleetDirection()
                break
    
    def runGame(self):
        """strting te main loop for the game"""
        while True:
            #helper methode
            self._checkEvents()

            if self.game_active:
                self.ship.updateShip()
                self.bullets.update()
                self._updateBullet()
                self._updateAliens()
                
            self._updateScreen()
            self.clock.tick(60) #set the frame rate

    def _checkEvents(self):
        """ respond to keypresses and mouse events """
        #wath for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mous_pos = pygame.mouse.get_pos()
                self._checkPlayButton(mous_pos)

    def _checkPlayButton(self , mous_pos):
        """ start a new game when the player clicks play """
        button_click = self.play_button.rect.collidepoint(mous_pos)

        #check the overlap of mous position and button and check inactivate game to click
        if button_click and not self.game_active:
            self.stats.resetStats() #reset the statistics of game (get 3 new ships)
            self.game_active = True

            #get rid of any remaning bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._createFleet()
            self.ship.centerShip()

            #hide the mous cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self , event):
        """ respond to keypresses """
        if event.key == pygame.K_RIGHT:
             #move the ship to the right
             self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fireBullet()
        elif event.key == pygame.K_q:
            sys.exit()

            
    def _check_keyup_events(self , event):
        """ respond to keypresses """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fireBullet(self):
        """ create a new bullet and add it in the bullet group """
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _updateScreen(self):
        """update images on the screen and flip to the new screen """
        #redraw the screen during neach pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.drawBullet()
        self.ship.blitMe()
        self.aliens.draw(self.screen)

        #draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.drawButton()

        #make the most recently drown screen visible
        pygame.display.flip()

    def _updateBullet(self):
        """ update position of bullets and get grid of old bullets """
        #grid of bullets that have disapeard
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._checkBulletAlienCollosions()

    def _checkBulletAlienCollosions(self):
        """ respond to bullet alien collisions """
        #remove any bullet and aliens that have collisions
        collisions = pygame.sprite.groupcollide(self.bullets , self.aliens , True , True)

        if not self.aliens:
            self.bullets.empty() #clear all sprites in the group
            self._createFleet() #make new aliens and show them in display


    def _updateAliens(self):
        """ update the positions of all aliens in the fleet """
        self._checkFleetEdges()
        self.aliens.update()

        #look for alien - ship collisions
        if pygame.sprite.spritecollideany(self.ship , self.aliens):
            self._shipHit()

        #look for aliens hitting the bottom of the screen
        self._checkAliensBottom()

    def _shipHit(self):
        """ respond to the ship being hit by an alien """
        if self.stats.ship_left > 0:
            #decrement ship_left
            self.stats.ship_left -= 1

            #get grid of any remaning bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._createFleet()
            self.ship.centerShip()

            #pouse
            sleep(2)
        
        else:
            self.game_active = False

    def _checkAliensBottom(self):
        """ check if any aliens reached the bottom of the screen """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #treat this the same as if the ship got hit
                self._shipHit()
                break
            
if __name__ == "__main__":
    #make a game instance and run the game
    ai = AlienInvasion()
    ai.runGame()
