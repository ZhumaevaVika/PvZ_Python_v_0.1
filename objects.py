import pygame as pg
from config import positions_y
from random import randint, choice, choices
from help_functions import type_handler, get_location_to_spawn
from player import player

sun_sprites = pg.sprite.Group()
suns = []
plants_sprites = pg.sprite.Group()
plants = []
bullet_sprites = pg.sprite.Group()
bullets = []
zombies_sprites = pg.sprite.Group()
zombies = []


def check_same_loc(plant):
    flag = True
    if plants:
        for obj in plants:
            if plant.pos == obj.pos:
                flag = False
    return flag


def spawn_plant(x, y, type='peashooter'):
    plant = None
    if get_location_to_spawn(x, y) and type:
        x, y = get_location_to_spawn(x, y)
        if type == 'peashooter':
            plant = PeaShooter(x, y)
        elif type == 'sunflower':
            plant = SunFlower(x, y)
        elif type == 'wallnut':
            plant = WallNut(x, y)
        elif type == 'potatomine':
            plant = PotatoMine(x, y)
        elif type == 'repeater':
            plant = Repeater(x, y)
        elif type == 'cherrybomb':
            plant = CherryBomb(x, y)
        elif type == 'torchwood':
            plant = Torchwood(x, y)
        elif type == 'firepeashooter':
            plant = FirePeaShooter(x, y)

        if check_same_loc(plant):
            if player.sun >= plant.cost:
                player.sun -= plant.cost
            plants_sprites.add(plant)
            plants.append(plant)
            return True
        else:
            del plant


def dig_plant(x, y):
    if get_location_to_spawn(x, y):
        x, y = get_location_to_spawn(x, y)
        for plant in plants:
            if plant.pos[0] == x and plant.pos[1] == y:
                plant.die()
                return True


def produce_sun_sky(shoot_delay, reload):
    shoot_delay += 1
    if shoot_delay == reload:
        sun = Sun()
        sun_sprites.add(sun)
        suns.append(sun)

        shoot_delay = 0
        reload = randint(480, 1000)
    return shoot_delay, reload


"""class Interface(pg.sprite.Sprite):
    def __init__(self, type):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (142, 50))
        if self.type == 'playersun':
            self.pos = (100, 30)
        else:
            self.pos = (300, 300)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, clicked):
        pass"""


class Plant(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.pos = (0, 0)

        self.type = None
        self.scale = (70, 70)
        self.if_damaged = 0
        self.if_damaged_counter = 0
        self.shoot_delay = 0
        self.reload = randint(81, 90)
        self.HP = 300
        self.maxHP = self.HP
        self.cost = 100
        self.arming_time = 840
        self.arming_timer = 0
        self.explode_time = 20
        self.explode_timer = 0
        self.explode_damage = 1800

    def update(self):
        self.damage_animation()
        self.shoot_delay += 1
        self.shoot('peashooter_bullet')

    def if_zombie(self):
        for zom in zombies:
            delta_y = (self.scale[1] - 70)/2 - 54
            if (zom.rect.y == self.rect.y + delta_y) and (zom.rect.x <= 1024):
                return True

    def shoot(self, type):
        if self.if_zombie():
            if self.shoot_delay >= self.reload:
                bullet = PeaShooterBullet(self, type)
                bullet_sprites.add(bullet)
                bullets.append(bullet)

                self.shoot_delay = 0
                self.reload = randint(81, 90)

    def produce_sun(self):
        if self.shoot_delay == self.reload:
            sun = SunF(self)
            sun_sprites.add(sun)
            suns.append(sun)

            self.shoot_delay = 0
            self.reload = randint(600, 1200)

    def check_hp_wallnut(self):
        if self.maxHP*0.25 <= self.HP <= self.maxHP*0.5:
            self.type = self.type[:-1] + '1'
        elif self.HP < self.maxHP*0.25:
            self.type = self.type[:-1] + '2'

    def arming(self):
        self.arming_timer += 1
        if (self.arming_timer >= self.arming_time) and (self.type == self.type[:-1] + '0'):
            self.type = self.type[:-1] + '1'
            filename = type_handler(self.type)
            self.image = pg.image.load(filename).convert_alpha()
            self.image = pg.transform.scale(self.image, self.scale)

    def explode(self):
        detonate = False
        if self.type == self.type[:-1] + '1':
            for zom in zombies:
                if (-10 <= self.rect.x - zom.rect.x + 25 <= 55) and (zom.rect.y == self.rect.y - 54):
                    self.type = self.type[:-1] + '2'
                    filename = type_handler(self.type)
                    self.image = pg.image.load(filename).convert_alpha()
                    self.image = pg.transform.scale(self.image, self.scale)
                    detonate = True
                if detonate and (-50 <= self.rect.x - zom.rect.x + 25 <= 95) and (zom.rect.y == self.rect.y - 54):
                    player.zombie_damaged += min(zom.HP, self.explode_damage)
                    zom.HP -= self.explode_damage
        if self.type == self.type[:-1] + '2':
            self.explode_timer += 1
            if self.explode_time == self.explode_timer:
                self.die()

    def big_explode(self):
        self.explode_timer += 1
        if (self.explode_time == self.explode_timer) and (self.type == self.type[:-1] + '1'):
            self.explode_timer = 0
            self.type = self.type[:-1] + '2'
            filename = type_handler(self.type)
            self.image = pg.image.load(filename).convert_alpha()
            self.image = pg.transform.scale(self.image, self.scale)
            for zom in zombies:
                if (-130 <= self.rect.x - zom.rect.x + 25 <= 175) and (-100 <= zom.rect.y - self.rect.y + 54 <= 100):
                    player.zombie_damaged += min(zom.HP, self.explode_damage)
                    zom.HP -= self.explode_damage

        if (self.type == self.type[:-1] + '2') and (self.explode_time == self.explode_timer):
            self.die()

    def fire_pea(self):
        for bullet in bullets:
            if ((bullet.type == 'peashooter_bullet') and (self.pos[0] + 35 >= bullet.rect.x >= self.pos[0] - 35)
                    and (bullet.rect.y == self.pos[1] - 31)):
                bullet.type = 'fire_pea'

    def damage_animation(self):
        if self.if_damaged == 1:
            self.if_damaged_counter += 1
            self.image.fill((3, 3, 3), special_flags=pg.BLEND_RGB_ADD)
            if self.if_damaged_counter >= 25:
                filename = type_handler(self.type)
                self.image = pg.image.load(filename).convert_alpha()
                self.image = pg.transform.scale(self.image, self.scale)

                self.if_damaged = 0
                self.if_damaged_counter = 0

    def die(self):
        plants.remove(self)
        self.kill()
        del self


class PeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'peashooter'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.reload = randint(81, 90)
        self.HP = 300
        self.cost = 100


class Repeater(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'repeater'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.reload = randint(81, 90)
        self.pause = 0
        self.HP = 300
        self.cost = 200

    def shoot(self, type):
        if self.if_zombie():
            if self.shoot_delay >= self.reload:
                bullet = PeaShooterBullet(self, type)
                bullet_sprites.add(bullet)
                bullets.append(bullet)

                self.pause = self.shoot_delay
                self.shoot_delay = 0
                self.reload = randint(81, 90)
            elif self.pause == self.reload + 15:
                bullet = PeaShooterBullet(self, type)
                bullet_sprites.add(bullet)
                bullets.append(bullet)

                self.pause = 0

    def update(self):
        self.damage_animation()
        self.shoot_delay += 1
        self.pause += 1
        self.shoot('peashooter_bullet')


class FirePeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'firepeashooter'
        self.scale = (90, 90)
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.reload = randint(81, 90)
        self.HP = 300
        self.cost = 175

    def update(self):
        self.damage_animation()
        self.shoot_delay += 1
        self.shoot('fire_pea')


class SunFlower(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'sunflower'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.reload = randint(600, 1200)
        self.HP = 300
        self.cost = 50

    def update(self):
        self.damage_animation()
        self.shoot_delay += 1
        self.produce_sun()


class WallNut(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'wallnut0'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.HP = 4000
        self.maxHP = self.HP
        self.cost = 50

    def update(self):
        self.check_hp_wallnut()
        self.damage_animation()


class PotatoMine(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'potatomine0'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.HP = 300
        self.maxHP = self.HP
        self.cost = 25

    def update(self):
        self.arming()
        self.explode()
        self.damage_animation()


class CherryBomb(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'cherrybomb1'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.HP = 300
        self.maxHP = self.HP
        self.cost = 150

    def update(self):
        self.big_explode()


class Torchwood(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'torchwood'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

        self.HP = 300
        self.maxHP = self.HP
        self.cost = 175

    def update(self):
        self.damage_animation()
        self.fire_pea()


class PeaShooterBullet(pg.sprite.Sprite):
    def __init__(self, peashooter, type='peashooter_bullet'):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        delta_y = None
        if self.type == 'peashooter_bullet':
            self.scale = (18, 18)
            self.damage = 20
            delta_y = -22
        elif self.type == 'fire_pea':
            self.scale = (44, 28)
            self.damage = 40
            delta_y = 2
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)
        self.pos = (peashooter.pos[0] + 35, peashooter.pos[1] + delta_y)
        self.rect = self.image.get_rect(center=self.pos)

        self.v = 7

    def update_type(self):
        if self.type == 'peashooter_bullet':
            self.scale = (18, 18)
            self.damage = 20
        elif self.type == 'fire_pea':
            self.scale = (44, 28)
            self.damage = 40

        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.scale)

    def update(self):
        self.update_type()
        self.move()
        self.damage_zombie()

    def die(self):
        bullets.remove(self)
        self.kill()
        del self

    def move(self):
        self.rect.x += self.v
        if self.rect.x > 1024:
            self.die()

    def damage_zombie(self):
        for zom in zombies:
            if (-10 <= zom.rect.x - self.rect.x + 25 <= 10) and (-20 <= zom.rect.y - self.rect.y + 58 <= 20):
                if self in bullets:
                    self.die()
                    player.zombie_damaged += min(zom.HP, self.damage)
                    zom.HP -= self.damage
                    zom.if_damaged = 1


class Sun(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'sky'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.pos = (randint(255, 960), 0)
        self.rect = self.image.get_rect(center=self.pos)

        self.shoot_delay = 0
        self.reload = randint(600, 1200)
        self.move_coord = randint(100, 550)
        self.flag = 0
        self.timer = 0
        self.v = 1

    def update(self, clicked):
        (x, y) = pg.mouse.get_pos()
        if self.flag == 1:
            self.timer += 1
        if self.timer >= 450:
            self.die()
        self.collect(x, y, clicked)
        self.move()

    def move(self):
        if self.type == 'sky':
            self.rect.y += self.v
            if self.rect.y == self.move_coord:
                self.v = 0
                self.flag = 1
        else:
            self.rect.y -= self.v
            if self.v >= 0:
                self.v -= 0.1
            else:
                self.v = 0
                self.flag = 1

    def collect(self, x, y, clicked):
        if ((self.rect.x + 25 - x)**2 + (self.rect.y + 25 - y)**2 <= 625) and clicked:
            if player.sun < 9900:
                player.sun += 50
            self.die()

    def die(self):
        suns.remove(self)
        self.kill()
        del self


class SunF(Sun):
    def __init__(self, sunflower):
        super().__init__()
        self.type = 'flower'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.pos = (sunflower.pos[0], sunflower.pos[1] - 40)
        self.rect = self.image.get_rect(center=self.pos)


def zombie_spawner(z, difficulty):
    zom = None
    if 0 <= difficulty <= 2:
        z = [z[0]]
        k = 1
    elif 3 <= difficulty <= 5:
        z = z[:1]
        k = 2
    elif 6 <= difficulty <= 8:
        z = z[:2]
        k = 3
    else:
        z = z
        k = 3
    if difficulty > 5:
        zom_arr = choices(z, k=5)
    else:
        zom_arr = choices(z, k=difficulty+1)

    if (player.timer % 30 == 0) and (player.timer >= 300):
        if zombies:
            sumHP = 0
            for zom in zombies:
                sumHP += zom.HP
            if sumHP <= 100*k:
                player.zombie_spawn = True
        else:
            player.zombie_spawn = True

    if player.zombie_spawn:
        for type in zom_arr:
            y = choice(positions_y) - 22
            if type == 'basiczombie':
                zom = BasicZombie(y)
            elif type == 'flagzombie':
                zom = FlagZombie(y)
            elif type == 'coneheadzombie':
                zom = ConeHeadZombie(y)
            elif type == 'bucketheadzombie':
                zom = BucketHeadZombie(y)

            zombies_sprites.add(zom)
            zombies.append(zom)
            player.zombie_spawn = False
        if difficulty <= 9:
            difficulty += 1
    return difficulty


def zombie_spawner_dev():
    for i in range(5):
        zom = BasicZombie(103 + 100*i)
        zombies_sprites.add(zom)
        zombies.append(zom)


class Zombie(pg.sprite.Sprite):
    def __init__(self, y=choice(positions_y)-22):
        pg.sprite.Sprite.__init__(self)
        delta_x = randint(0, 5)
        self.pos = (1070 + delta_x*25, y)
        # self.pos = (1070, 303)

        self.type = None
        self.state = 'move'
        self.if_damaged = 0
        self.if_damaged_counter = 0
        self.v = 0.25
        self.timer = 0
        self.HP = 190
        self.maxHP = self.HP
        self.damage = 50
        self.armor = self.HP - 190

    def update_base(self):
        plt = None
        if self.HP <= 0:
            self.die()
        for plt in plants:
            if (-10 <= plt.rect.x - self.rect.x + 25 <= 55) and (self.rect.y == plt.rect.y - 54):
                self.state = 'damage_plant'
                break
        self.damage_animation()
        if self.state == 'move':
            self.move()
        elif self.state == 'damage_plant':
            if plt.HP <= 0:
                plt.die()
                for zom in zombies:
                    zom.state = 'move'
            self.timer += 1
            if 55 < self.timer < 60:
                plt.HP -= self.damage
                plt.if_damaged = 1
                self.timer = 0

    def update_type(self):
        if (100 <= self.HP <= 190) and ((self.type == 'bucketheadzombie2') or (self.type == 'coneheadzombie2')):
            self.type = 'basiczombie0'
        elif 0 <= self.HP < 100:
            self.type = 'basiczombie1'
        elif (self.maxHP - self.armor//3 >= self.HP >= self.maxHP - self.armor*2//3) and (self.type != 'basiczombie0'):
            self.type = self.type[:-1] + '1'
        elif (self.maxHP - self.armor*2//3 >= self.HP >= self.maxHP - self.armor) and (self.type != 'basiczombie0'):
            self.type = self.type[:-1] + '2'

    def update(self):
        self.update_base()
        self.update_type()

    def move(self):
        self.timer += self.v
        if self.timer > 1:
            self.rect.x -= 1
            self.timer = 0

    def damage_animation(self):
        if self.if_damaged == 1:
            self.if_damaged_counter += 1
            self.image.fill((3, 3, 3), special_flags=pg.BLEND_RGB_ADD)
            if self.if_damaged_counter >= 25:
                filename = type_handler(self.type)
                self.image = pg.image.load(filename).convert_alpha()
                self.image = pg.transform.scale(self.image, (90, 135))
                self.if_damaged = 0
                self.if_damaged_counter = 0

    def die(self):
        zombies.remove(self)
        self.kill()
        del self


class BasicZombie(Zombie):
    def __init__(self, y=choice(positions_y)-22):
        super().__init__(y)
        self.type = 'basiczombie0'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'move'
        self.v = 0.25
        self.HP = 190


class FlagZombie(Zombie):
    def __init__(self, y=choice(positions_y)-22):
        super().__init__(y)
        self.type = 'flagzombie1'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'move'
        self.v = 0.25
        self.HP = 190


class ConeHeadZombie(Zombie):
    def __init__(self, y=choice(positions_y)-22):
        super().__init__(y)
        self.type = 'coneheadzombie0'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'move'
        self.v = 0.25
        self.HP = 560
        self.maxHP = self.HP
        self.armor = self.HP - 190


class BucketHeadZombie(Zombie):
    def __init__(self, y=choice(positions_y)-22):
        super().__init__(y)
        self.type = 'bucketheadzombie0'
        filename = type_handler(self.type)
        self.image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'move'
        self.v = 0.25
        self.HP = 1290
        self.maxHP = self.HP
        self.armor = self.HP - 190
