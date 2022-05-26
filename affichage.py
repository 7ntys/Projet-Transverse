import pygame
import pytmx
import pyscroll
from player import Player


class Game:

    def __init__(self):
        # crée la fenètre pygame
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("Jeu")

        # génère la map
        tmx_data = pytmx.util_pygame.load_pygame('map_3.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 0.44
        face = "right"
        player_position = tmx_data.get_object_by_name("spawn")
        self.player = Player(player_position.x, player_position.y)
        self.player.location = player_position.x, player_position.y

        #  crée une liste d'objets de collide
        self.collide_bas = []
        self.collide_bas_pos_y = []
        self.collide_bas_height = []
        for obj in tmx_data.objects:
            if obj.type == "collision_bas":
                self.collide_bas.append(pygame.Rect(obj.x+400, obj.y, obj.width, obj.height))
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
    def input(self,face):
        face = "right"
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True,face
        if pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()
            #self.player.change_animation('left')
            face = "left"
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
            face = "right"
        return False,face    

    def update(self,face):
        #Return 0 = Aucune collision
        #Return 1 = Touche un sol
        #Return 2 = Touche un mur
        self.group.update()
        for sprite in self.group.sprites():
            if self.player.rect.collidelist(self.collide) != -1 and self.player.rect.collidelist(self.collide_bas) != -1:
                sprite.move_back(self.collide_pos_y[sprite.rect.collidelist(self.collide)],
                self.collide_height[sprite.rect.collidelist(self.collide)])
                self.player.move_back_right(face)
                return 1
            if self.player.rect.collidelist(self.collide) != -1:
                sprite.move_back(self.collide_pos_y[sprite.rect.collidelist(self.collide)],
                                 self.collide_height[sprite.rect.collidelist(self.collide)])                             
                return 1
            if self.player.rect.collidelist(self.collide_bas) != -1:
                #sprite.move_back_bas()
                self.player.move_back_right(face)
                
                return 2
            else:
                return 0

    def run(self):
        clock = pygame.time.Clock()
        running = True
        t = 0
        jumping = False
        can_jump = True
        g = 1.5
        face = "right"
        while running:
            clock.tick(60)
            self.player.save_location()
            x,y = self.player.update_rect()
            collide = self.update(face)
            space_pressed,face = self.input(face)
            #if space_pressed:
                #print("                   space_pressed :           ",space_pressed)
            #print("can jump      :",can_jump)
            if collide == 1:
                #print("COLLIDE")
                can_jump = True
                jumping = False
                t = 0
                g = 2
            if space_pressed and can_jump:
                self.player.jump(t)
                jumping = True
                can_jump = False
            elif not jumping and collide != 1:
                if g < 5:
                    g *= 1.5
                if g >= 5 and g <= 10: 
                    g *= 1.05      
                self.player.gravity(g)
                can_jump = False
            if jumping:
                g = 2
                t += 1
                self.player.jump(t)
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            a_x = (self.player.position[0]/10240)*1920
            a_y = ((self.player.position[1]/7680)*1080)-400
            #print("calcul x :",a_x)
            #print("calcul y :",a_y)
            #print("position x et y ",self.player.position[0],"et", self.player.position[1])
            self.screen.blit(self.player.sprite, (a_x,a_y))
            pygame.draw.rect(self.screen, (255,0,0), self.player.rect,2)
            #show_hitbox(self.screen,self.collide_bas)
            b = pygame.image.load('red_square.jpg').convert()
            b = pygame.transform.scale(b,(165,292))
            #self.screen.blit(b, (x,y))
            #pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(x,y,165,292),2)
            #a = pygame.image.load('red_square.jpg').convert()
            #a = pygame.transform.scale(a,(200,354))
            #self.screen.blit(a,(0,0))
            pygame.display.flip()
            check_input_exit()
           
        pygame.quit()

def check_input_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                exit()        

def show_hitbox(win,list_hitbox):
    b = pygame.image.load('red_square.jpg').convert()
    for a in list_hitbox:
        a.x = (a.x/10240)*1920
        a.y = ((a.y/7680)*1080)-400
        print(a.x)
        win.blit(b, (a.x,a.y))
        pygame.draw.rect(win, (255,0,0), pygame.Rect(a.x,a.y, a.width,a.height),2)

