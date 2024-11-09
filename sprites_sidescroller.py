#this file was created by: Rohan Yarrakonda
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random


vec = pg.math.Vector2

class Player(Sprite):       
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        # self.rect.x = x
        # self.rect.y = y
        #self.x = x * TILESIZE
        #self.y = y * TILESIZE
        self.pos = vec(x* TILESIZE, y * TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        self.jumping = False
        self.jump_power = 25
        # self.vx, self.vy = 0, 0
        self.coins = 0
    
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #   self.vy -= self.speed
        if keys[pg.K_a]:
            self.vx -= self.speed
        #if keys[pg.K_s]:
        #    self.vy += self.speed
        if keys[pg.K_d]:
            self.vx += self.speed
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        print("I'm trying to jump...")
        print(self.vel.y)
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
        
    def collide_with_walls(self, dir):
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.x = hits[0].rect.left - TILESIZE
                    # self.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.vel.y = hits[0].rect.top - TILESIZE
                    # self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                print("i hit a powerup...")
                self.speed += 1.5
            if str(hits[0].__class__.__name__) == "Coin":
                print("I hit a coin...")
                self.coins += 1
            if str(hits[0].__class__.__name__) == "Portal":
                print("I hit a portal...")
                self.game.activate_portal()

    def update(self):
        self.acc= vec(0,GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # reverse order to fix collision issues
        
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)

        self.rect.x = self.x
        self.collide_with_walls('x')
        
        self.rect.y = self.y
        self.collide_with_walls('y')
        
        # reverse order to fix collision issues
        



class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
        self.category = random.choice([0,1])
    
    def update(self):
     
        # moving towards the side of the screen
        self.rect.x += self.speed
        # when it hits the side of the screen, it will move in opposite direction

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        
        if hits:
            # print("off the screen...")
            self.speed *= -1
            self.rect.y += 32
        if self.rect.right > WIDTH or self.rect.left < 0:
            # print("off the screen...")
            self.speed *= -1
            self.rect.y += 32
        # elif self.rect.colliderect(self.game.player):
        #     self.speed *= -1
        # elif self.rect.colliderect(self):
        #     self.speed *= -1
        

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLACK)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Portal(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PURPLE)  # Change color as needed for the portal
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass



