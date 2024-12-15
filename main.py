#this file was made by:Rohan Yarrakonda
#this code was created by: Rohan Yarrakonda
#a use of Blackbox AI in one part as cited

#import all needed libraries and modules
import pygame as pg

#from settings import *
from sprites_sidescroller import *
from sprites import *
from tilemap import *
from os import path
import time

import sys
from random import randint



'''
Elevator pitch: 

GOALS : Collect all the coins to win
RULES : You have to evade the mobs so you do not die and there are boundaries due to walls. You have powerups that can win you the game. 
FEEDBACK:  If you touch the mobs, then you die.
FREEDOM : You have no restrictions on movement and you can move inside the game space


'''

# created a game class to instantiate later

# this class is there to organize the elements needed to create a gam
class Game:
    # init initializes all the needed parts for the game
    
        
    def __init__(self):
        pg.init()  # Initialize all Pygame modules
        pg.mixer.init() 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Initialize the screen (video system)
        pg.display.set_caption("Rohan's Game") #window title
        self.clock = pg.time.Clock()
        self.running = True
        self.portal_active = False #  Track if the portal effect is active
        self.invulnerable_time = 0 #timer for invulnerability
        self.invulnerable = False  # Initially, player is not invulnerable

        
    # Activate the portal, making the player invulnerable for a short time
    def activate_portal(self):
        self.portal_active = True
        self.invulnerable = True  # Player becomes invulnerable
        self.invulnerable_time = time.time()  # Start the timer for 5 seconds
        print("Portal activated! Player is now invulnerable.")
 
    # create player block, creates the all_sprites group so that we can batch update and render, defines properties that can be seen in the game system
    
    # Load game data, including the map
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    # Create new game elements
    def new(self):
        self.load_data()
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()

        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # self.player = Player(self, 1, 1)
        # instantiated a mob
        # self.mob = Mob(self, 100,100)
        # makes new mobs and walls using a for loop
        # for i in range(randint(10,20)):
        #     m = Mob(self, i*randint(0, 200), i*randint(0, 200))
        #     Wall(self, i*TILESIZE, i*TILESIZE)


        # Create game elements based on the map data
        for row, tiles in enumerate(self.map.data):
            print(row) # Print the current row for debugging
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                elif tile == 'T':  
                    Portal(self, col, row)
    
    # using self.running as a boolean to continue running the game
   

    #draw the game elements on the screen
    def draw(self):
        if self.portal_active:
            self.screen.fill(BLACK)  # Change background to black
        else:
         self.screen.fill(WHITE)  # Default background color
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt * 1000), 24, WHITE, WIDTH / 30, HEIGHT / 30)
        self.draw_text(self.screen, "This game is awesome...", 24, BLACK, WIDTH / 2, HEIGHT / 24)
        pg.display.flip() # Update the display
   
    #main game loop 
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # Limit the frame rate and calculate delta time
            self.events()
            self.update()
            self.draw()

        pg.quit()
        # input
    
    # Looks for any events
    
    def events(self):
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        # pg.quit()

        # process
    
    def update(self):
         
       # Check if the invulnerability period has passed
        if self.invulnerable and time.time() - self.invulnerable_time > 5:
            self.invulnerable = False
            self.portal_active = False  # Reset portal background after 5 seconds
            print("Invulnerability expired.")
        
        self.all_sprites.update()
        # Other update logic

        #use of blackbox ai
        #len returns the number of characters in a string
        if self.player.coins == len(self.all_coins): #checks if all coins are collected
            self.show_win_screen() # Show win screen if all coins are collected
    
    # Show the win screen when the player wins
    def show_win_screen(self):
        self.screen.fill(WHITE)
        self.draw_text(self.screen, "You Win!", 40, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()  # Wait for a key press to continue    

   
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color) # Render the text
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect) # Draw the text on the surface
    
    # Draw all sprites 
    def draw (self):
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(pg.time.get_ticks()), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "Coins collected: " + str(self.player.coins), 24, BLACK, WIDTH/2, HEIGHT/24)
      
        
        if self.portal_active:  # If portal effect is active
            self.screen.fill(BLACK)  # Change background to black
        else:
            self.screen.fill(WHITE)  # Default background color
        
        self.all_sprites.draw(self.screen)
        pg.display.flip()  # Flip the screen to update the display


    
    def show_death_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "Game Over", 40, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()  # Wait for a key press to continue


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS) # Limit frame rate 
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False # Exit waiting loop
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False # Exit waiting loop on key press






if __name__ == "__main__":
    g = Game() #Create a new game instance
    # create all game elements with the new method
    g.new()
    # run the game
    g.run()
    #showing deathscreen
    g.show_death_screen()
