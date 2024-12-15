#this file created by: Rohan Yarrakonda


import pygame as pg
from pygame.sprite import Sprite
import random
from settings import *

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 25
        self.vx, self.vy = 0, 0
        self.coins = 0
        self.health = 100
        self.dir = ''
        self.invulnerable = False  # New attribute for invulnerability state
        self.invulnerable_time = 0  # To track time when invulnerability started
        self.jumps = 0 #set initial jump count
    
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:  # Assuming "W" is the jump key
            if self.jumps < 2:  # Allow double jump
                self.vy = -self.speed  # Set upward velocity
                self.jumps += 1  # Increment jump count

        # Reset jump count when on the ground
        if self.rect.bottom >= HEIGHT:  # Assuming ground is at the bottom of the screen
            self.jumps = 0  # Reset jumps when on the ground

        if keys[pg.K_a]:
            self.vx -= self.speed
        if keys[pg.K_s]:
            self.vy += self.speed
        if keys[pg.K_d]:
            self.vx += self.speed
        if keys[pg.K_LSHIFT]:
            self.get_dir()
            print(self.dir)

    def get_dir(self):
        #Determine the direction of movement based on velocity
        if abs(self.vx) > abs(self.vy):
            if self.vx > 0:
                self.dir = (1, 0)
            elif self.vx < 0:
                self.dir = (-1, 0)         
        if abs(self.vy) > abs(self.vx):
            if self.vy > 0:
                self.dir = (0, 1)
            elif self.vy < 0:
                self.dir = (0, -1) 
    
    def collide_with_mobs(self):
            #Check for collisions with mobs
            hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
            if hits:
                print("Player hit by mob. game over")
                self.game.show_death_screen() 

    def collide_with_walls(self, dir):
        #Handle collisions with walls
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - TILESIZE
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0 ## Stop horizontal movement
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - TILESIZE
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0 # Stop vertical movement
                self.rect.y = self.y


    def collide_with_stuff(self, group, kill):
        #Check for collisions with specified group and handle them
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Powerup":
                print("I hit a powerup...")
                self.speed += 1.5 # Increase speed if a powerup is hit
            if str(hits[0].__class__.__name__) == "Coin":
                print("I hit a coin...")
                self.coins += 1 # Increment coin count
            if str(hits[0].__class__.__name__) == "Portal":
                print("I hit a portal...")
                self.activate_invulnerability()  # Activate invulnerability when hitting the portal

    def activate_invulnerability(self):
        """Activates invulnerability for 5 seconds."""
        self.invulnerable = True
        self.invulnerable_time = pg.time.get_ticks()  #  the time when invulnerability started

    def check_collisions(self):
        if pg.sprite.spritecollide(self.player, self.mobs, False):
        # Collision detected
            self.player.health -= 10  # Reduce health
            print("Collision detected! Player health:", self.player.health)
        if self.player.health <= 0:
            self.game_over()  # Trigger game over logic

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        # Apply gravity
        if self.rect.bottom < HEIGHT:  # If not on the ground
            self.vy += 1  # Apply gravity
        
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_mobs, True)

        self.rect.x = self.x
        self.collide_with_walls('x')
        
        self.rect.y = self.y
        self.collide_with_walls('y')

        # Check if the invulnerability time has passed (5 seconds)
        if self.invulnerable and pg.time.get_ticks() - self.invulnerable_time > 5000:
            self.invulnerable = False  # End invulnerability after 5 seconds
        
        if self.rect.bottom >= HEIGHT:
            self.jumps = 0

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)#  Initialize the Sprite class with the group
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)  # Set wall color
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups) #  Initialize the Sprite class with the group
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10  #Set the initial speed of the mob
        self.category = random.choice([0, 1])

    def collide_with_stuff(self, group, kill):
        # Check for collisions with a specified group of sprites
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                print("Mob hit a powerup...")
                self.speed += 1.5  # Increase speed if a powerup is hit
            if str(hits[0].__class__.__name__) == "Coin":
                print("Mob hit a coin...")

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.speed > 0:
                    self.rect.x = hits[0].rect.left - TILESIZE
                if self.speed < 0:
                    self.rect.x = hits[0].rect.right
                self.speed = -self.speed #Reverse speed to change direction
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.rect.bottom > hits[0].rect.top:
                    self.rect.bottom = hits[0].rect.top
                if self.rect.top < hits[0].rect.bottom:
                    self.rect.top = hits[0].rect.bottom

    def update(self):
        # Move the mob left or right
        self.rect.x += self.speed
        
        # Check for collisions with powerups, coins, and other objects
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)

        # Handle collisions with walls in the x direction
        self.collide_with_walls('x')

        # Handle collisions with walls in the y direction
        self.collide_with_walls('y')

        # If the mob hits a wall, reverse its direction
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            self.speed *= -1
            self.rect.y += 32  # Move down a little to avoid getting stuck in the wall
        
        # Reverse direction if the mob goes out of bounds horizontally
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed *= -1
            self.rect.y += 32  # Move down when reversing direction

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups) #initialize the Sprite class with the groups
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)   #color
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Portal(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups) #initialize the Sprite class with the groups
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PURPLE)  # color
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups) #initialize the Sprite class with the groups
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect() #rectangle area of the portal
        self.image.fill(YELLOW)  # color
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE #x position based on the grid
        self.rect.y = y * TILESIZE #y position based on the grid

    def update(self):
        pass  # No changes needed for this class unless for some portal animation
