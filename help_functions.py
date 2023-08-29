from config import positions_x, positions_y


def get_location_to_spawn_y(y):
    for i in range(5):
        if 80 + i * 100 <= y <= 180 + i * 100:
            return positions_y[i], i


def get_location_to_spawn(x, y):
    try:
        for i in range(9):
            if 255 + i * 77 <= x <= 335 + i * 77:
                y, j = get_location_to_spawn_y(y)
                x = positions_x[i]
                return x, y
    except:
        return None


def reduce_brightness(image, coef):
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, a = image.get_at((x, y))
            new_r = int(r * coef)
            new_g = int(g * coef)
            new_b = int(b * coef)
            image.set_at((x, y), (new_r, new_g, new_b, a))


'''
def brighter_cell(image):
    (x, y) = pg.mouse.get_pos()
    try:
        i = -1
        for k in range(9):
            if 255 + k * 77 <= x <= 335 + k * 77:
                y, j = get_location_to_spawn_y(y)
                i = k
        if i != -1:
            for x in range(255+i*77, 335+i*77):
                for y in range(80 + i * 100, 180 + i * 100):
                    r, g, b, a = image.get_at((x, y))
                    new_r = int(r * 1.5)
                    new_g = int(g * 1.5)
                    new_b = int(b * 1.5)
                    image.set_at((x, y), (new_r, new_g, new_b, a))

    except:
        return None
'''


def type_handler(type):
    filename, reload_time = None, None
    if type == 'sunflower_seed':
        filename = 'sprites/SunFlowerSeed.png'
        reload_time = 300
        cost = 50
        size = (81, 55)
    elif type == 'peashooter_seed':
        filename = 'sprites/PeaShooterSeed.png'
        reload_time = 300
        cost = 100
        size = (81, 55)
    elif type == 'potatomine_seed':
        filename = 'sprites/PotatoMineSeed.png'
        reload_time = 1200
        cost = 25
        size = (81, 55)
    elif type == 'wallnut_seed':
        filename = 'sprites/WallNutSeed.png'
        reload_time = 1200
        cost = 50
        size = (81, 55)
    elif type == 'repeater_seed':
        filename = 'sprites/Repeater_seed.png'
        reload_time = 300
        cost = 200
        size = (81, 55)
    elif type == 'cherrybomb_seed':
        filename = 'sprites/CherryBombSeed.png'
        reload_time = 2100
        cost = 150
        size = (81, 55)
    elif type == 'torchwood_seed':
        filename = 'sprites/Torchwood_seed.png'
        reload_time = 300
        cost = 175
        size = (81, 55)
    elif type == 'firepeashooter_seed':
        filename = 'sprites/FirePeashooter_seed.png'
        reload_time = 300
        cost = 175
        size = (81, 55)
    elif type == 'button_shovel':
        filename = 'sprites/Shovel.png'
        reload_time = 10
        cost = 0
        size = (70, 70)
    elif type == 'button_pause':
        filename = 'sprites/Pause.png'
        reload_time = 10
        cost = 0
        size = (70, 70)
    elif type == 'button_speedup':
        filename = 'sprites/SpeedUp.png'
        reload_time = 10
        cost = 0
        size = (70, 70)
    elif type == 'button_resume':
        filename = 'sprites/Resume.png'
        reload_time = 10
        cost = 0
        size = (151, 47)
    elif type == 'button_restart':
        filename = 'sprites/Restart.png'
        reload_time = 10
        cost = 0
        size = (151, 47)

    elif type == 'pause_menu':
        filename = 'sprites/PauseMenu.png'

    elif type == 'playersun':
        filename = 'sprites/PlayerSun.png'

    elif type == 'sunflower':
        filename = 'sprites/SunFlower.png'
    elif type == 'peashooter':
        filename = 'sprites/PeaShooter.png'
    elif type == 'wallnut0':
        filename = 'sprites/WallNut0.png'
    elif type == 'wallnut1':
        filename = 'sprites/WallNut1.png'
    elif type == 'wallnut2':
        filename = 'sprites/WallNut2.png'
    elif type == 'potatomine0':
        filename = 'sprites/PotatoMine0.png'
    elif type == 'potatomine1':
        filename = 'sprites/PotatoMine1.png'
    elif type == 'potatomine2':
        filename = 'sprites/PotatoMine2.png'
    elif type == 'repeater':
        filename = 'sprites/Repeater.png'
    elif type == 'cherrybomb1':
        filename = 'sprites/CherryBomb0.png'
    elif type == 'cherrybomb2':
        filename = 'sprites/CherryBomb1.png'
    elif type == 'torchwood':
        filename = 'sprites/Torchwood.png'
    elif type == 'firepeashooter':
        filename = 'sprites/FirePeashooter.png'

    elif type == 'peashooter_bullet':
        filename = 'sprites/PeashooterBullet.png'
    elif type == 'fire_pea':
        filename = 'sprites/FirePea.png'

    elif type == 'basiczombie0':
        filename = 'sprites/Zombie0.png'
    elif type == 'basiczombie1':
        filename = 'sprites/Zombie1.png'
    elif type == 'flagzombie1':
        filename = 'sprites/FlagZombie.png'
    elif type == 'coneheadzombie0':
        filename = 'sprites/ConeHeadZombie0.png'
    elif type == 'coneheadzombie1':
        filename = 'sprites/ConeHeadZombie1.png'
    elif type == 'coneheadzombie2':
        filename = 'sprites/ConeHeadZombie2.png'
    elif type == 'bucketheadzombie0':
        filename = 'sprites/BucketHeadZombie0.png'
    elif type == 'bucketheadzombie1':
        filename = 'sprites/BucketHeadZombie1.png'
    elif type == 'bucketheadzombie2':
        filename = 'sprites/BucketHeadZombie2.png'

    elif type == 'flower' or type == 'sky':
        filename = 'sprites/Sun.png'
    if (type[-4:] == 'seed') or (type[:6] == 'button'):
        return filename, reload_time, cost, size
    else:
        return filename
