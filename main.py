import pygame as pg
from game import game


def main():
    while not game.exit_program:
        if game.state == 'run_level':
            game.run_level()
        elif game.state == 'select_plants_screen':
            game.select_plant_screen()
        elif game.state == 'level_select_screen':
            game.level_select_screen()
        elif game.state == 'main_menu':
            game.main_menu()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
