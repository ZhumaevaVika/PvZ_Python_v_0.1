import pygame as pg


def draw_sun(screen):
    font = pg.font.SysFont(None, 48)
    img = font.render(str(int(player.sun)), True, (255, 255, 255))
    screen.blit(img, (90, 15))


class Player:
    def __init__(self, dev_mode):
        self.plant_type = None
        self.zombie_damaged = 0
        self.timer = 0
        self.zombie_spawn = False
        self.plants = []
        self.plants_prev = ['sunflower_seed', 'peashooter_seed', 'potatomine_seed', 'wallnut_seed', 'repeater_seed',
              'cherrybomb_seed', 'torchwood_seed']
        if dev_mode:
            self.sun = 9900
        else:
            self.sun = 0

    def update(self, screen):
        self.timer += 1
        draw_sun(screen)


player = Player(False)
