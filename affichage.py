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
        tmx_data = pytmx.util_pygame.load_pygame('final_map.tmx')
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
                    self.player.sprite_number = 1
                    return True,face
 
        if pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.run = True
            face = "left"
        elif not(pressed[pygame.K_d] or pressed[pygame.K_RIGHT]):
            self.player.run = False        
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.run = True
            face = "right"
        elif not(pressed[pygame.K_q] or pressed[pygame.K_LEFT]):
            self.player.run = False
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

    def check_input_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    exit()  

    def run(self):
        self.menu(0)
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
            if collide == 1:
                can_jump = True
                jumping = False
                t = 0
                g = 2
            if space_pressed and can_jump:
                self.player.jump(t)
                self.player.jump_sprite(t)
                jumping = True
                can_jump = False
                self.player.run = True
            elif not jumping and collide != 1:
                if g < 5:
                    g *= 1.5
                if g >= 5 and g <= 10: 
                    g *= 1.05      
                self.player.gravity(g)
                can_jump = False
                self.player.run = False
            if jumping:
                g = 2
                t += 1
                self.player.jump(t)
                self.player.run = True
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            a_x = (self.player.position[0]/20480)*1920
            a_y = ((self.player.position[1]/10240)*1080)
            #print("calcul x :",a_x)
            #print("calcul y :",a_y)
            #print("position x et y ",self.player.position[0],"et", self.player.position[1])
            print(self.player.run)
            if self.player.run == False:
                self.player.idle()
            self.player.good_face(face)    
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
            self.check_input_exit()
           
        pygame.quit()
  

    def show_hitbox(win,list_hitbox):
        b = pygame.image.load('red_square.jpg').convert()
        for a in list_hitbox:
            a.x = (a.x/20480)*1920
            a.y = ((a.y/10240)*1080)-400
            print(a.x)
            win.blit(b, (a.x,a.y))
            pygame.draw.rect(win, (255,0,0), pygame.Rect(a.x,a.y, a.width,a.height),2)

    def display_text(self, text, positionX, positionY, size,R,G,B):    #Fonction texte
        font = pygame.font.SysFont("arial", size)                     #Police et taille
        font.set_bold(True)                                   
        text = font.render(text, True, (R, G, B), None)               #Couleur
        self.screen.blit(text, (positionX, positionY))                        #Position du texte

    def menu(self,b):               #779 640 (bas gauche)  487 (haut gauche) 1036,487 (haut droite) 1036,640
        clock = pygame.time.Clock()
        self.parallax_load()

        actual_screen = pygame.image.load("tileset/Interface/Screen1.png").convert_alpha()
        actual_screen = pygame.transform.scale(actual_screen, (1920, 1080))  
        button_play = pygame.draw.rect(self.screen, (0, 200, 200), (780,  487, 257, 153))
        button_settings = pygame.draw.rect(self.screen, (0, 200, 0), (780,  680, 257, 153))
        button_leave = pygame.draw.rect(self.screen, (200, 200, 0), (780,  876, 257, 153))
        while b == 0:   

            clock.tick(300)        
            button_play = pygame.draw.rect(self.screen, (0, 200, 200), (780,  487, 257, 153))               
            button_settings = pygame.draw.rect(self.screen, (0, 200, 0), (780,  680, 257, 153))
            button_leave = pygame.draw.rect(self.screen, (200, 200, 0), (780,  876, 257, 153))
            self.parallax()
            self.screen.blit(actual_screen, (0, 0)) 
            pygame.display.flip()
            event = pygame.event.poll()                                                              #Evenement = attendre
            if event.type == pygame.KEYDOWN:                                                         
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos                                                                  #position de la souris = la position ou t'as cliqué 
                if button_play.collidepoint(mouse_pos): 
                    b = 1
                    break
                if button_settings.collidepoint(mouse_pos):            
                    b = self.menu_return(b,mouse_pos)
                if button_leave.collidepoint(mouse_pos):
                    exit()
        
    def menu_return(self,b,mouse_pos):
        clock = pygame.time.Clock()
        actual_screen = pygame.image.load("tileset/Interface/Screen2.png").convert_alpha()  
        actual_screen = pygame.transform.scale(actual_screen, (1920, 1080))  
        while b == 0 :
            clock.tick(300)  
            button_leave = pygame.draw.rect(self.screen, (200, 200, 200), (780,  876, 257, 153))
            button_son = pygame.draw.rect(self.screen, (0, 200, 0), (769,  497, 290, 243))
            self.parallax()
            self.screen.blit(actual_screen, (0, 0)) 
            pygame.display.flip()
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:                                                         
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos    
                if button_son.collidepoint(mouse_pos):
                    print("Son on/off")                      
                if button_leave.collidepoint(mouse_pos):
                    b = 0
                    return b
                    self.menu()
                    button_play = pygame.draw.rect(win, (0, 200, 200), (780,  487, 257, 153))        

    def parallax_load(self):
        self.tree = pygame.image.load("tileset/Interface/menu/layers/tree.png").convert_alpha()
        self.tree =  pygame.transform.scale(self.tree, (1088, 320)) 
        self.treex = 0
        self.treefarx = 0
        self.mountainx = 0
        self.mountainfarx = 0
        self.treefar = pygame.image.load("tileset/Interface/menu/layers/treefar.png").convert_alpha()
        self.treefar =  pygame.transform.scale(self.treefar, (1700, 500)) 
        self.mountain = pygame.image.load("tileset/Interface/menu/layers/mountain.png").convert_alpha()     
        self.mountain =  pygame.transform.scale(self.mountain, (952, 560))    
        self.mountainfar = pygame.image.load("tileset/Interface/menu/layers/mountainfar.png").convert_alpha()
        self.mountainfar =  pygame.transform.scale(self.mountainfar, (1428, 840)) 
        self.sky = pygame.image.load("tileset/Interface/menu/layers/sky.png").convert_alpha()        
        self.sky =  pygame.transform.scale(self.sky, (1920, 1080)) 

    def parallax(self):
        self.screen.blit(self.sky, (0,0))
        #---------------------------------------------------------
        self.screen.blit(self.mountainfar, (self.mountainfarx+1000,200))
        self.screen.blit(self.mountainfar, (self.mountainfarx-1000,200))
        self.screen.blit(self.mountainfar, (self.mountainfarx,200))
        self.screen.blit(self.mountainfar, (self.mountainfarx+2000,200))
        #---------------------------------------------------------
        self.screen.blit(self.mountain, (self.mountainx,500))
        self.screen.blit(self.mountain, (self.mountainx+1000,530))
        self.screen.blit(self.mountain, (self.mountainx-1000,500))
        self.screen.blit(self.mountain, (self.mountainx+2000,525))
        #---------------------------------------------------------
        self.screen.blit(self.treefar, (self.treefarx+1500,600))
        self.screen.blit(self.treefar, (self.treefarx+1000,600))
        self.screen.blit(self.treefar, (self.treefarx+700,600))
        self.screen.blit(self.treefar, (self.treefarx+300,600))
        self.screen.blit(self.treefar, (self.treefarx-300,600))
        self.screen.blit(self.treefar, (self.treefarx-600,600))
        #---------------------------------------------------------
        self.screen.blit(self.tree, (self.treex,760))
        self.screen.blit(self.tree, (self.treex+1000,760))
        self.screen.blit(self.tree, (self.treex+700,760))
        self.screen.blit(self.tree, (self.treex+300,760))
        self.screen.blit(self.tree, (self.treex-300,760))
        self.screen.blit(self.tree, (self.treex-600,760))
        #---------------------------------------------------------
        self.treex += 0.2
        self.treefarx += 0.1
        self.mountainx += 0.05
        self.mountainfarx += 0.025
        if self.treex >= 780:
            self.treex = -544
        if self.treefarx >= 780:
            self.treex = -544    