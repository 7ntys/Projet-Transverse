from telnetlib import XASCII
import pygame
from pygame import Surface


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load('tileset/BlueWizard/BlueWizard_Walk/Chara_BlueWalk1.png').convert_alpha()
        self.scale = [165,292]
        self.sprite = pygame.transform.scale(self.sprite,(self.scale[0],self.scale[1]))
        self.position = [x, y]
        self.image = self.get_image()
        #self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        #self.rect = pygame.Rect((self.position[0]/20480)*1920,((self.position[1]/10240)*1080)-400,self.scale[0],self.scale[1])

        self.run = False
        self.speed = 10
        self.g = 100
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

    def move_right(self):
        self.position[0] += self.speed
        self.sprite =  self.change_sprite()
        self.run = True
    def move_left(self):
        self.position[0] -= self.speed
        self.sprite = self.change_sprite()
        self.run = True

    def jump(self, t):
        self.position[1] -= ((self.speed+4)*t)-1/2*self.g*t**2

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
    def get_image(self):
        image: Surface = pygame.Surface(([self.scale[0],self.scale[1]]))
        return image
            
    def idle(self): #changer le sprite en "Idle"
        self.sprite = pygame.image.load('tileset/BlueWizard/BlueWizard_Idle/Chara - BlueIdle' + str(self.sprite_number) + ".png").convert_alpha()  
        self.sprite = pygame.transform.scale(self.sprite,(self.scale[0],self.scale[1]))
        self.sprite_loop += 1
        if self.sprite_loop >= 8:
            self.sprite_number += 1
            self.sprite_loop = 0
        if self.sprite_number >= 20:
            self.sprite_number = 1
        return self.sprite   
    def change_sprite(self): #changer le sprite en "Marche"
        self.sprite = pygame.image.load('tileset/BlueWizard/BlueWizard_Walk/Chara_BlueWalk' + str(self.sprite_number) + ".png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,(self.scale[0],self.scale[1]))
        self.sprite_loop += 1

        if self.sprite_loop >= 10:
            self.sprite_number += 1
            self.sprite_loop = 0
        if self.sprite_number >= 20:
            self.sprite_number = 1
        return self.sprite  

    def jump_sprite(self,t): #changer le sprite en "Saut"
        self.sprite = pygame.image.load('tileset/BlueWizard/BlueWizard_Jump/CharaWizardJump_' + str(self.sprite_number) + ".png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,(self.scale[0],self.scale[1]))
        #self.image.set_colorkey([0, 0, 0])
        self.sprite_loop += 1
            
        if self.sprite_loop >= 20:
            self.sprite_number += 1
            self.sprite_loop = 0
        if self.sprite_number >= 8:
            self.sprite_number = 1
        if self.speed+4 >= -1/2*self.g*t**2: 
            if self.sprite_number >= 5:
                self.sprite_number = 5
        else: 
            if self.sprite_number <= 5:
                self.sprite_number = 5
        return self.sprite  


    def update_rect(self): #update du rectangle avec redimension
        self.rect.move((self.position[0]/20480)*1920,((self.position[1]/10240)*1080)-400)
        return ((self.position[0]/20480)*1920),(((self.position[1]/10240)*1080-400))

    def good_face(self,face): #Orienter le sprite en fonction de la direction ou il regarde
        if face == "left":
            self.sprite = pygame.transform.flip(self.sprite, True, False)
