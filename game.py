import pygame as pg
from objects import zombie_spawner, produce_sun_sky, plants_sprites, plants, bullet_sprites, bullets, zombies_sprites, \
    zombies, sun_sprites, suns, player
from buttons import interfaces, interface_sprites, buttons, buttons_sprites, spawn_buttons, spawn_pause_menu, \
    spawn_level_interface, spawn_main_menu_buttons, spawn_level_select_buttons, SelectPlantsScreen, LetsRockButton, Back2Button, spawn_select_plants_buttons, spawn_empty_slots, ResetButton
from config import WIDTH, HEIGHT, z
from random import randint

pg.init()


class Game:
    def __init__(self):
        self.state = 'main_menu'
        self.FPS = 60
        self.background = None
        self.clock = None
        self.screen = None
        self.exit_program = False

    def run_level(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background = pg.image.load("sprites/Frontyard.png")
        paused = False

        spawn_buttons(player.plants)

        spawn_level_interface()

        sky_sun_reload = randint(480, 1000)
        sky_sun_delay = sky_sun_reload - 150
        difficulty = 0
        run = True
        while run:
            clicked = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_program = True
                    return
                elif event.type == pg.MOUSEBUTTONDOWN:
                    clicked = 1

            if not paused:
                sky_sun_delay, sky_sun_reload = produce_sun_sky(sky_sun_delay, sky_sun_reload)
                difficulty = zombie_spawner(z, difficulty)
                for zom in zombies:
                    zom.update()
                for plt in plants:
                    plt.update()
                for bul in bullets:
                    bul.update()
                for sun in suns:
                    sun.update(clicked)
                for button in buttons:
                    button.update(clicked)
            for butt in interfaces:
                butt.update(clicked)
                if butt.type == 'button_speedup':
                    if butt.state == 'hold_plant':
                        self.FPS = 120
                    else:
                        self.FPS = 60
                if butt.type == 'button_pause':
                    if (butt.state == 'hold_plant') and not paused:
                        resume, restart, exit_level = spawn_pause_menu()
                        paused = True

                if (butt.type == 'pause_menu') or (butt.type == 'button_resume') or (butt.type == 'button_restart') or (
                        butt.type == 'button_exit_level'):
                    if resume.state == 'pressed':
                        butt.die_interface()
                        paused = False
                    if restart.state == 'pressed':
                        paused = False
                        run = False
                    if exit_level.state == 'pressed':
                        butt.die_interface()
                        paused = False
                        self.state = 'level_select_screen'
                        player.plants_prev = player.plants.copy()
                        player.plants.clear()
                        run = False

            self.screen.blit(self.background, (0, 0))
            plants_sprites.draw(self.screen)
            zombies_sprites.draw(self.screen)
            bullet_sprites.draw(self.screen)
            sun_sprites.draw(self.screen)
            buttons_sprites.draw(self.screen)
            interface_sprites.draw(self.screen)
            player.update(self.screen)
            pg.display.update()
            pg.display.flip()
            self.clock.tick(self.FPS)
        self.restart(buttons)
        if self.state == 'run_level':
            self.run_level()

    def restart(self, buttons):
        while len(zombies) + len(plants) + len(bullets) + len(suns) + len(buttons) + len(interfaces) > 0:
            for zom in zombies:
                zom.die()
            for plt in plants:
                plt.die()
            for bul in bullets:
                bul.die()
            for sun in suns:
                sun.die()
            for button in buttons:
                button.die()
            for butt in interfaces:
                interfaces.remove(butt)
                butt.kill()
                del butt
        player.sun = 0

    def reset_player_plants(self, buttons):
        while len(buttons) > 19:
            for button in buttons:
                if button.type[-4:] == 'seed':
                    buttons.remove(button)
                    button.kill()
                    del button

    def select_plant_screen(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background = pg.image.load("sprites/FrontyardCopy.png")

        obj = SelectPlantsScreen()
        buttons.append(obj)
        buttons_sprites.add(obj)

        lets_rock = LetsRockButton()
        buttons.append(lets_rock)
        buttons_sprites.add(lets_rock)

        back2 = Back2Button()
        buttons.append(back2)
        buttons_sprites.add(back2)

        '''reset = ResetButton()
        buttons.append(reset)
        buttons_sprites.add(reset)'''

        spawn_empty_slots(7)
        spawn_select_plants_buttons()

        run = True
        while run:
            clicked = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_program = True
                    return
                elif event.type == pg.MOUSEBUTTONDOWN:
                    clicked = 1

            for button in buttons:
                button.update(clicked)
                if back2.state == 'pressed':
                    button.die()
                    self.state = 'level_select_screen'
                    run = False
                if (lets_rock.state == 'pressed') and (len(player.plants) == 0):
                    lets_rock.state = 'normal'
                if lets_rock.state == 'pressed':
                    button.die()
                    self.state = 'run_level'
                    run = False
                '''if reset.state == 'pressed':
                    player.plants = player.plants_prev'''

                if (button.type[-4:] == 'slot') and (button.state == 'hold_plant') and (button.chosen == False) and (len(player.plants) < 7):
                    player.plants.append(button.type[:-5])
                    button.chosen = True
                    self.reset_player_plants(buttons)
                    spawn_buttons(player.plants)
                if (button.type[-4:] == 'slot') and ((button.state == 'filled') or (button.state == 'normal')) and (button.chosen == True):
                    player.plants.remove(button.type[:-5])
                    button.chosen = False
                    self.reset_player_plants(buttons)
                    spawn_buttons(player.plants)
                if (len(player.plants) == 7) and (button.state == 'hold_plant') and (button.type[:-5] not in player.plants):
                    button.state = 'normal'

            self.screen.blit(self.background, (0, 0))
            buttons_sprites.draw(self.screen)
            pg.display.update()
            pg.display.flip()
            self.clock.tick(self.FPS)
        self.restart(buttons)

    def level_select_screen(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background = pg.image.load("sprites/LevelSelectScreen.png")

        filenames = ['button_level_zombie', 'button_level_cone', 'button_level_bucket', 'button_level_pole', 'button_level_flag']
        back = spawn_level_select_buttons(filenames)

        run = True
        while run:
            clicked = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_program = True
                    return
                elif event.type == pg.MOUSEBUTTONDOWN:
                    clicked = 1

            for button in buttons:
                button.update(clicked)
                if back.state == 'pressed':
                    self.state = 'main_menu'
                    run = False
                elif buttons[0].state == 'pressed':
                    self.state = 'select_plants_screen'
                    run = False
                elif buttons[1].state == 'pressed':
                    self.state = 'select_plants_screen'
                    run = False
                elif buttons[2].state == 'pressed':
                    self.state = 'select_plants_screen'
                    run = False
                elif buttons[3].state == 'pressed':
                    self.state = 'select_plants_screen'
                    run = False
                elif buttons[4].state == 'pressed':
                    self.state = 'select_plants_screen'
                    run = False
                if button.state == 'pressed':
                    while len(buttons) > 0:
                        for butt in buttons:
                            butt.die()


            self.screen.blit(self.background, (0, 0))
            buttons_sprites.draw(self.screen)
            pg.display.update()
            pg.display.flip()
            self.clock.tick(self.FPS)

    def main_menu(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background = pg.image.load("sprites/MainMenu.png")

        spawn_buttons([])

        play, survival, exit = spawn_main_menu_buttons()

        run = True
        while run:
            clicked = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_program = True
                    return
                elif event.type == pg.MOUSEBUTTONDOWN:
                    clicked = 1

            for button in buttons:
                button.update(clicked)
                if play.state == 'pressed':
                    button.die()
                    self.state = 'level_select_screen'
                    run = False
                if survival.state == 'pressed':
                    button.die()
                    self.state = 'select_plants_screen'
                    run = False
                if exit.state == 'pressed':
                    button.die()
                    self.exit_program = True
                    return

            self.screen.blit(self.background, (0, 0))
            buttons_sprites.draw(self.screen)
            pg.display.update()
            pg.display.flip()
            self.clock.tick(self.FPS)

        self.restart(buttons)


game = Game()
