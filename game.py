import pygame as pg
from objects import zombie_spawner_dev, Interface, interfaces, interface_sprites, Shovel, zombie_spawner, spawn_buttons, produce_sun_sky, plants_sprites, plants, bullet_sprites, bullets, \
    zombies_sprites, zombies, sun_sprites, suns, player, PauseButton, PauseMenuSprite, PauseMenuButtonResume, PauseMenuButtonRestart, SpeedUpButton
from config import WIDTH, HEIGHT, z
from random import randint
pg.init()
class Game():
    def __init__(self):
        self.state = 'run_level'
        self.FPS = 60

    def run_level(self):
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()
        background = pg.image.load("sprites/Frontyard.png")
        paused = False

        buttons, buttons_sprites = spawn_buttons(
            ['sunflower_seed', 'peashooter_seed', 'potatomine_seed', 'wallnut_seed', 'repeater_seed', 'cherrybomb_seed',
             'torchwood_seed', 'firepeashooter_seed'])
        shovel = Shovel()
        buttons.append(shovel)
        buttons_sprites.add(shovel)

        pause = PauseButton()
        interfaces.append(pause)
        interface_sprites.add(pause)

        speed_up = SpeedUpButton()
        interfaces.append(speed_up)
        interface_sprites.add(speed_up)


        # zombie_spawner_dev()

        player_sun = Interface('playersun')
        interfaces.append(player_sun)
        interface_sprites.add(player_sun)

        sky_sun_reload = randint(480, 1000)
        sky_sun_delay = sky_sun_reload - 150
        difficulty = 0
        while True:
            clicked = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.MOUSEMOTION:
                    pass
                elif event.type == pg.KEYDOWN:
                    pass
                elif event.type == pg.MOUSEBUTTONDOWN:
                    clicked = 1

            if pg.mouse.get_pressed()[0]:
                pass

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
                        pause_menu = PauseMenuSprite()
                        interfaces.append(pause_menu)
                        interface_sprites.add(pause_menu)

                        resume = PauseMenuButtonResume()
                        interfaces.append(resume)
                        interface_sprites.add(resume)

                        restart = PauseMenuButtonRestart()
                        interfaces.append(restart)
                        interface_sprites.add(restart)

                        paused = True

                if butt.type == 'button_resume':
                    resume = butt
                if butt.type == 'button_restart':
                    restart = butt

                if (butt.type == 'pause_menu') or (butt.type == 'button_resume') or (butt.type == 'button_restart'):
                    if resume.state == 'pressed':
                        interfaces.remove(butt)
                        butt.kill()
                        del butt
                        paused = False
                    if restart.state == 'pressed':
                        interfaces.remove(butt)
                        butt.kill()
                        del butt
                        paused = False
                        # self.restart(buttons) # FIXME
                        # self.run_level()


            screen.blit(background, (0, 0))
            plants_sprites.draw(screen)
            zombies_sprites.draw(screen)
            bullet_sprites.draw(screen)
            sun_sprites.draw(screen)
            buttons_sprites.draw(screen)
            interface_sprites.draw(screen)
            player.update(screen)
            pg.display.update()
            pg.display.flip()
            clock.tick(self.FPS)

    def restart(self, buttons):
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
    def main_menu(self):
        pass


game = Game()
