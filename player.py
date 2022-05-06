import pygame
from pygame import Surface


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 2
        self.g = 0.01
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def position(self):
        pos = self.position
        return pos

    def accelerate(self):
        self.speed = 4

    def decelerate(self):
        self.speed = 2

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def jump(self, t):
        self.position[1] -= (self.speed+4)-1/2*self.g*t**2

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position

    def move_back(self, y, height):
        self.position[0] = self.old_position[0]
        self.position[1] = y-height-16.1
        self.rect.topleft = self.position

    def gravity(self, g):
        self.position[1] += g

    def get_image(self, x, y):
        image: Surface = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
