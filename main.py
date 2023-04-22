import pygame
from constans import *
from parts.menu import Menu
from parts.arrows.arrow_manager import Arrows
from parts.healthbar import Health
from parts.raven import Raven
from parts.score import Score
from utils import Time_Manager


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),)
pygame.display.set_caption("Raven Flight")
font = pygame.font.Font('freesansbold.ttf', 32)


arrows = Arrows()
health_bar = Health()
score = Score(font)
raven = Raven()


def handle_fire_arrow():
    arrows.add_arrow(raven.current_position)


def reset():
    arrows.reset()
    health_bar.reset()
    score.reset()
    raven.reset()
    time_manager.reset()


menu = Menu(reset, font)
menu.show_initial_menu(screen)

time_manager = Time_Manager(
    handle_fire_arrow, raven.change_sprite_frame, score.increase_score)


run = True
while run and menu.run:
    screen.fill(BG)

    arrows.render_arrows(screen)
    health_bar.show_healthbars(screen)
    score.show_score(screen)
    raven.show_raven(screen)

    health_bar.check_collision_and_lower_hp(
        arrows.on_move_arrows(raven.current_position))
    raven.change_position()

    time_manager.tick()

    if health_bar.hps == 0:
        menu.show_played_menu(screen, score.score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            raven.change_directions(event)
    pygame.display.update()
pygame.quit()
