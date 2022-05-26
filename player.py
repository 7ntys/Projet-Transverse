from telnetlib import XASCII
import pygame
from pygame import Surface


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load('tileset/BlueWizard/BlueWizard_Idle/Chara - BlueIdle1.png').convert_alpha()
        self.scale = [165,292]
        self.sprite = pygame.transform.scale(self.sprite,(self.scale[0],self.scale[1]))
        self.position = [x, y]
        self.image = self.get_image()
        #self.image.set_colorkey([0, 0, 0])
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect((self.position[0]/10240)*1920,((self.position[1]/7680)*1080)-400,self.scale[0],self.scale[1])


        self.speed = 10
        self.g = 0.002
        self.sprite_number = 1
        self.sprite_loop = 10
        #self.images = {
            #'left': self.get_image(0, 100),
            #'right': self.get_image(0, 100),
        #}
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def position1(self):
        pos = self.position
        return pos

    #def change_animation(self, name):
        #self.image = self.images[name]
        #self.image.set_colorkey([0, 0, 0])

    def move_right(self):
        self.position[0] += self.speed
        self.sprite =  self.change_sprite()
    def move_left(self):
        self.position[0] -= self.speed
        self.sprite = self.change_sprite()

    def jump(self, t):
        self.position[1] -= (self.speed+4)-1/2*self.g*t**2

    def update(self):
        self.rect.topleft = self.position

    def move_back(self, y, height):
        self.position[0] = self.old_position[0]
        self.position[1] = y-height-self.scale[1]+2
        self.rect.topleft = self.position

    def move_back_bas(self):
        self.position[0] = self.old_position[0]
        self.position[1] = self.old_position[1] + 1
        self.rect.topleft = self.position

    def move_back_right(self,face):
        if face == "left":
            self.position[0] += self.speed
        elif face == "right":
            self.position[0] -= self.speed    
    def gravity(self, g):
        self.position[1] += g
        print("gravité")
    def get_image(self):
        image: Surface = pygame.Surface(([self.scale[0],self.scale[1]]))
        return image
            

    def change_sprite(self):
        self.sprite = pygame.image.load('tileset/BlueWizard/BlueWizard_Idle/Chara - BlueIdle' + str(self.sprite_number) + ".png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,(self.scale[0],self.scale[1]))
        #self.image.set_colorkey([0, 0, 0])
        self.sprite_loop += 1

        if self.sprite_loop >= 10:
            self.sprite_number += 1
            self.sprite_loop = 0
        if self.sprite_number >= 20:
            self.sprite_number = 1
        return self.sprite  

    def update_rect(self):
        self.rect.move((self.position[0]/10240)*1920,((self.position[1]/7680)*1080)-400)
        return ((self.position[0]/10240)*1920),(((self.position[1]/7680)*1080)-400)
