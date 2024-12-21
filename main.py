#this file was made by:Rohan Yarrakonda
#this code was created by: Rohan Yarrakonda
#use of Chat GPT 

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
        self.invulnerable = False  # Initially player is not invulnerable
        self.game_state = "playing"  

        
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
        self.game_state = "playing"
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
            self.dt = self.clock.tick(FPS) / 1000  # Limit the frame rate and calculate delta time
            self.events()
            self.update()
            self.draw()

            # Check game state to show win or lose screen
            if self.game_state == "won":
                self.show_win_screen()
                break  # Exit the loop after showing the win screen
            elif self.game_state == "lost":
                self.show_death_screen()
                break  # Exit the loop after showing the death screen

        pg.quit()

        

      
        # input
    
    # Looks for any events
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False  # Just set running to False to exit the game loop
        # pg.quit()

        # process
    
    def update(self):
         
       # Check if the invulnerability period has passed
        if self.invulnerable and time.time() - self.invulnerable_time > 5:
            self.invulnerable = False
            self.portal_active = False

        self.all_sprites.update()

    # Check for collisions with mobs
        self.player.collide_with_mobs()

    # Check if all coins are collected
        if self.player.coins == len(self.all_coins):
            self.game_state = "won"  # Set game state to won

             


    
      

   
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    
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


    #use of chat gpt
        #len returns the number of characters in a string
        if self.player.coins == len(self.all_coins): #checks if all coins are collected
            self.show_win_screen() # Show win screen if all coins are collected
    
    def show_win_screen(self):
        self.screen.fill(WHITE)
        self.draw_text(self.screen, "You Win!", 40, BLACK, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()  # Wait for a key press to continue
        

    def show_death_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "You Died", 40, WHITE, WIDTH/ 2, HEIGHT/2)
        pg.display.flip()
        pg.quit()
        self.wait_for_key()
    


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False






if __name__ == "__main__":
    g = Game()
    # create all game elements 
    g.new()
    
    g.run()

    g.show_death_screen()

pg.quit()
