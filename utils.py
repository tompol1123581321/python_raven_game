import pygame
from constans import *


def get_image(sheet, width, height, scale, colour, start_position, rotation=0):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (start_position[0]*width,
               start_position[1] * height, (start_position[0]+1)*width, (start_position[1]+1)*height))
    image = pygame.transform.scale(image, (width*scale, height * scale))
    image = pygame.transform.rotate(image, rotation)
    image.set_colorkey(colour)
    return image


def check_collision(raven_position, arrow_position):
    arrow_point = (
        arrow_position[0] + ARROW_SPRITE_WIDTH * ARROW_SCALE / 2, arrow_position[1] + ARROW_SPRITE_HEIGHT * ARROW_SCALE / 2)
    xIsInCollision = arrow_point[0] > raven_position[0] and arrow_point[0] < raven_position[0] + \
        RAVEN_SPRITE_WIDTH * SCALE

    yisInCollision = arrow_point[1] > raven_position[1] and arrow_point[1] < raven_position[1] + \
        RAVEN_SPRITE_HEIGHT * SCALE
    return xIsInCollision and yisInCollision


class Time_Manager:
    def __init__(self, fire_arrow_fun, update_raven_fun, increase_score_fun):
        self.time_elapsed_since_last_animation_change = 0
        self.time_elapsed_since_last_arrow_fired = 0
        self.time_elapsed_since_incresed_score = 0
        self.clock = pygame.time.Clock()
        self.fire_arrow_fun = fire_arrow_fun
        self.update_raven_fun = update_raven_fun
        self.increase_score_fun = increase_score_fun
        self.arrow_speed = 4000

    def tick(self):
        dt = self.clock.tick()
        [anim, arr, score] = [dt, dt, dt]
        self.time_elapsed_since_last_animation_change += anim
        self.time_elapsed_since_last_arrow_fired += arr
        self.time_elapsed_since_incresed_score += score

        if self.time_elapsed_since_last_animation_change > MOVEMENT_SPEED * 50:
            self.update_raven_fun()
            self.time_elapsed_since_last_animation_change = 0

        if self.time_elapsed_since_last_arrow_fired > MOVEMENT_SPEED * self.arrow_speed:
            self.fire_arrow_fun()
            self.time_elapsed_since_last_arrow_fired = 0

        if self.time_elapsed_since_incresed_score > MOVEMENT_SPEED * 4000:
            self.increase_score_fun()
            self.arrow_speed = self.arrow_speed-50
            self.time_elapsed_since_incresed_score = 0

    def reset(self):
        self.time_elapsed_since_last_animation_change = 0
        self.time_elapsed_since_last_arrow_fired = 0
        self.time_elapsed_since_incresed_score = 0
        self.clock = pygame.time.Clock()
        self.arrow_speed = 4000
