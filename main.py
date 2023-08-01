import pygame as pg
from objects import zombie_spawner_dev, Interface, interfaces, interface_sprites, Shovel, zombie_spawner, spawn_buttons, produce_sun_sky, plants_sprites, plants, bullet_sprites, bullets, \
    zombies_sprites, zombies, sun_sprites, suns, player
from config import FPS, WIDTH, HEIGHT, z
from random import randint
pg.init()

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    background = pg.image.load("sprites/Frontyard.png")

    buttons, buttons_sprites = spawn_buttons(['sunflower_seed', 'peashooter_seed', 'potatomine_seed', 'wallnut_seed', 'repeater_seed', 'cherrybomb_seed', 'torchwood_seed', 'firepeashooter_seed'])
    shovel = Shovel()
    buttons.append(shovel)
    buttons_sprites.add(shovel)

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
        clock.tick(FPS)



if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
