import pygame as pg
from help_functions import type_handler, reduce_brightness
from objects import spawn_plant, dig_plant
from player import player
from config import all_plants

buttons_sprites = pg.sprite.Group()
buttons = []
interface_sprites = pg.sprite.Group()
interfaces = []


def spawn_buttons(filenames):
    for i in range(len(filenames)):
        button = Buttons(filenames[i], i)
        buttons_sprites.add(button)
        buttons.append(button)
    return buttons, buttons_sprites


def spawn_select_plants_buttons():
    for i in range(len(all_plants)):
        button = SelectPlantsButtons(all_plants[i], i)
        buttons_sprites.add(button)
        buttons.append(button)
    return buttons, buttons_sprites


def spawn_empty_slots(amount):
    for i in range(amount):
        slot = EmptySlotSprite(i)
        buttons_sprites.add(slot)
        buttons.append(slot)
    return buttons, buttons_sprites


def spawn_pause_menu():
    pause_menu = PauseMenuSprite()
    interfaces.append(pause_menu)
    interface_sprites.add(pause_menu)

    resume = PauseMenuButtonResume()
    interfaces.append(resume)
    interface_sprites.add(resume)

    restart = PauseMenuButtonRestart()
    interfaces.append(restart)
    interface_sprites.add(restart)

    exit_level = PauseMenuButtonMainMenu()
    interfaces.append(exit_level)
    interface_sprites.add(exit_level)

    return resume, restart, exit_level


def spawn_level_interface():
    shovel = Shovel()
    buttons.append(shovel)
    buttons_sprites.add(shovel)

    pause = PauseButton()
    interfaces.append(pause)
    interface_sprites.add(pause)

    speed_up = SpeedUpButton()
    interfaces.append(speed_up)
    interface_sprites.add(speed_up)

    player_sun = Interface('playersun')
    interfaces.append(player_sun)
    interface_sprites.add(player_sun)


def spawn_level_select_buttons(filenames):
    for i in range(len(filenames)):
        button = LevelButton(filenames[i], i)
        buttons_sprites.add(button)
        buttons.append(button)

    back = BackButton()
    buttons.append(back)
    buttons_sprites.add(back)

    return back


def spawn_main_menu_buttons():
    play = PlayButton()
    buttons.append(play)
    buttons_sprites.add(play)

    survival = SurvivalButton()
    buttons.append(survival)
    buttons_sprites.add(survival)

    exit = ExitButton()
    buttons.append(exit)
    buttons_sprites.add(exit)

    return play, survival, exit


class Interface(pg.sprite.Sprite):
    def __init__(self, type):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.filename = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (142, 50))
        if self.type == 'playersun':
            self.pos = (100, 30)
        else:
            self.pos = (300, 300)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, clicked):
        pass


class Buttons(pg.sprite.Sprite):
    def __init__(self, type, number):
        pg.sprite.Sprite.__init__(self)
        self.filename, self.reload_time, self.cost, self.size = type_handler(type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.pos = (100, 80 + number*55 + 3)
        self.rect = self.image.get_rect(center=self.pos)

        self.type = type
        self.state = 'normal'
        self.timer = -1

    def update(self, clicked):
        self.button_animation()
        self.click(clicked)

    def reload_animation(self):
        if self.timer % (self.reload_time/10) == 0:
            n = 10 - int(self.timer // (self.reload_time/10))
            for x in range(self.image.get_width()):
                for y in range(n*5, (n+1)*5):
                    r, g, b, a = self.image.get_at((x, y))
                    new_r = int(r * 1.5)
                    new_g = int(g * 1.5)
                    new_b = int(b * 1.5)
                    self.image.set_at((x, y), (new_r, new_g, new_b, a))

    def button_animation(self):
        (x, y) = pg.mouse.get_pos()
        if self.state == 'normal' and player.sun < self.cost:
            reduce_brightness(self.image, 0.35)
            self.state = 'not_enough_sun'
        if self.state == 'not_enough_sun' and player.sun >= self.cost:
            self.state = 'normal'
        if ((self.rect.x <= x <= self.rect.x + self.size[0]) and (self.rect.y <= y <= self.rect.y + self.size[1])
                and self.state == 'normal'):
            self.image = pg.image.load(self.filename).convert_alpha()
            self.image = pg.transform.scale(self.image, self.size)
            self.image.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
            self.state = 'filled'
        elif not((self.rect.x <= x <= self.rect.x + self.size[0]) and
                 (self.rect.y <= y <= self.rect.y + self.size[1])) and self.state == 'filled':
            self.state = 'normal'
        elif self.state == 'pressed':
            reduce_brightness(self.image, 0.35)
            self.state = 'hold_plant'
        elif self.state == 'normal':
            self.image = pg.image.load(self.filename).convert_alpha()
            self.image = pg.transform.scale(self.image, self.size)
        elif self.state == 'reload':
            self.timer += 1
            self.reload_animation()
            if self.timer == self.reload_time:
                self.state = 'normal'
                self.timer = -1

    def click(self, clicked):
        (x, y) = pg.mouse.get_pos()
        if (self.state == 'filled') and clicked:
            self.state = 'pressed'
            player.plant_type = self.type[:-5]
        elif (self.state == 'hold_plant') and clicked:
            if spawn_plant(x, y, player.plant_type):
                self.state = 'reload'
            else:
                self.state = 'normal'

    def die(self):
        buttons.remove(self)
        self.kill()
        del self

    def die_interface(self):
        interfaces.remove(self)
        self.kill()
        del self


class Shovel(Buttons):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_shovel'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (70, 70))
        self.pos = (975, 565)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1

    def click(self, clicked):
        (x, y) = pg.mouse.get_pos()
        if (self.state == 'filled') and clicked:
            self.state = 'pressed'
        elif (self.state == 'hold_plant') and clicked:
            if dig_plant(x, y):
                self.state = 'reload'
            else:
                self.state = 'normal'


class PauseButton(Buttons):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_pause'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (975, 40)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1

    def click(self, clicked):
        (x, y) = pg.mouse.get_pos()
        if (self.state == 'filled') and clicked:
            self.state = 'pressed'
        elif (self.state == 'hold_plant') and clicked:
            if ((658 <= x <= 802) or (453 <= x <= 598) or (248 <= x <= 392)) and (385 <= y <= 430):
                self.state = 'normal'


class SpeedUpButton(Buttons):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_speedup'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (895, 40)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1

    def click(self, clicked):
        (x, y) = pg.mouse.get_pos()
        if (self.state == 'filled') and clicked:
            self.state = 'pressed'
        elif (self.state == 'hold_plant') and clicked:
            if ((self.pos[0] - self.size[0]//2 <= x <= self.pos[0] + self.size[0]//2)
                    and (self.pos[1] - self.size[1]//2 <= y <= self.pos[1] + self.size[1]//2)):
                self.state = 'normal'


class SelectPlantsButtons(SpeedUpButton):
    def __init__(self, type, number):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type, True)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.pos = (238 + (number % 4)*92, 130 + (number//4)*55)
        self.rect = self.image.get_rect(center=self.pos)
        self.type = self.type + '_slot'
        self.chosen = False

        self.state = 'normal'
        self.timer = -1


class ResetButton(SpeedUpButton):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_reset'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type, True)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.pos = (100, 468)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class EmptySlotSprite(pg.sprite.Sprite):
    def __init__(self, number):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_empty'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.pos = (100, 80 + number*55 + 3)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1

    def die(self):
        buttons.remove(self)
        self.kill()
        del self


class PauseMenuSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'pause_menu'
        self.filename = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (638, 317))
        self.pos = (525, 275)
        self.rect = self.image.get_rect(center=self.pos)

    def die(self):
        buttons.remove(self)
        self.kill()
        del self

    def die_interface(self):
        interfaces.remove(self)
        self.kill()
        del self


class SelectPlantsScreen(PauseMenuSprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'select_plants_screen'
        self.state = 'none'
        self.filename = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (419, 419))
        self.pos = (375, 255)
        self.rect = self.image.get_rect(center=self.pos)


class PauseMenuButtonResume(Buttons):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_resume'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (705, 400)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1

    def click(self, clicked):
        if (self.state == 'filled') and clicked:
            self.state = 'pressed'


class PauseMenuButtonRestart(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_restart'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (500, 400)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class PauseMenuButtonMainMenu(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_exit_level'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (295, 400)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class LevelButton(Buttons):
    def __init__(self, type, number):
        pg.sprite.Sprite.__init__(self)
        self.filename, self.reload_time, self.cost, self.size = type_handler(type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.pos = (110 + (number % 5)*200, 120 + (number//5)*250)
        self.rect = self.image.get_rect(center=self.pos)

        self.type = type
        self.state = 'normal'
        self.timer = -1

    def click(self, clicked):
        if (self.state == 'filled') and clicked:
            self.state = 'pressed'


class BackButton(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_back'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (100, 550)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class Back2Button(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_back2'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (200, 550)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class LetsRockButton(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_lets_rock'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (970, 550)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class PlayButton(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_play'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (500, 250)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class SurvivalButton(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_survival'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (500, 300)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1


class ExitButton(PauseMenuButtonResume):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'button_exit'
        self.filename, self.reload_time, self.cost, self.size = type_handler(self.type)
        self.image = pg.image.load(self.filename).convert_alpha()
        self.pos = (500, 350)
        self.rect = self.image.get_rect(center=self.pos)

        self.state = 'normal'
        self.timer = -1
