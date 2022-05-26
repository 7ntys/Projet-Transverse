from affichage import Game
from player import *

def musique():
    musique = 'tileset/final_map_assets/music.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(musique)
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play(-1)


if __name__ == '__main__':
    pygame.init()
    musique()
    game = Game()
    game.run()
                