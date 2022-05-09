import pygame
import pytmx
import pyscroll
from player import Player


class Game:

    def __init__(self):
        # crée la fenètre pygame
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption("Jeu")

        # génère la map
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        player_position = tmx_data.get_object_by_name("spawn")
        self.player = Player(player_position.x, player_position.y)
        self.player.location = player_position.x, player_position.y

        #  crée une liste d'objets de collide
        self.collide_bas = []
        self.collide_bas_pos_y = []
        self.collide_bas_height = []
        for obj in tmx_data.objects:
            if obj.type == "collision_bas":
                self.collide_bas.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                self.collide_bas_pos_y.append(obj.y)
                self.collide_bas_height.append(obj.height)

        self.collide = []
        self.collide_pos_y = []
        self.collide_height = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collide.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                self.collide_pos_y.append(obj.y)
                self.collide_height.append(obj.height)

        # met a jour les layers du dessin
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)

    # récupère les entrées de l'utilisateur
    def input(self):
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        if pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def update(self):
        self.group.update()
        for sprite in self.group.sprites():
            if sprite.rect.collidelist(self.collide) != -1:
                sprite.move_back(self.collide_pos_y[sprite.rect.collidelist(self.collide)],
                                 self.collide_height[sprite.rect.collidelist(self.collide)])
                print("haut")
                return True
            elif sprite.rect.collidelist(self.collide_bas) != -1:
                sprite.move_back_bas()
                print("bas")
                return True
            else:
                return False

    def run(self):
        clock = pygame.time.Clock()
        running = True
        t = 0
        jumping = False
        can_jump = True
        g = 0
        while running:
            self.player.save_location()
            collide = self.update()
            space_pressed = self.input()
            if space_pressed and can_jump:
                jumping = True
            if collide:
                can_jump = True
                jumping = False
                t = 0
                g = 1.5
            elif not jumping:
                g *= 1.15
                self.player.gravity(g)
                can_jump = False
            if jumping:
                t += 1
                self.player.jump(t)
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()
            pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if pressed[pygame.K_ESCAPE]:
                    running = False
            clock.tick(60)
        pygame.quit()
