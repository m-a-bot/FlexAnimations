import arcade
from animations.animation import Animation
from settings import *
import math
from animations.animation import FiguresType
import numpy as np


def move_cart_to_center(x, y):
    return x - WIDTH // 2, y - HEIGHT // 2


def move_cart_to_origin(x, y):
    return x + WIDTH // 2, y + HEIGHT // 2


def polar_to_cart(r, phi):
    x = r * math.cos(phi)
    y = r * math.sin(phi)

    return x, y


def cart_to_polar(x, y):
    phi = math.atan2(y, x)
    r = math.sqrt(x ** 2 + y ** 2)

    return r, phi


def increase_angle(x, y, inc):
    x, y = move_cart_to_center(x, y)
    r, phi = cart_to_polar(x, y)
    phi += inc
    x, y = polar_to_cart(r, phi)
    x, y = move_cart_to_origin(x, y)
    return x, y


class Tornado(Animation):
    def __init__(self, figure_type):
        super().__init__(figure_type)
        self.speed = 1
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.center = (self.center_x, self.center_y)

        if figure_type == FiguresType.CIRCLE:
            self.texture = "resources/icons/Круг.png"
        if figure_type == FiguresType.TRIANGLE:
            self.texture = "resources/icons/Треугольник.png"
        if figure_type == FiguresType.SQUARE:
            self.texture = "resources/icons/Квадрат.png"
        self.texture = 'resources/icons/current_figure.png'


    def fill_sprites(self, sprites):
        super().fill_sprites(sprites)
        # x, y = move_cart_to_center(*self.center)
        # r, phi = cart_to_polar(x, y)
        distances_delta = [75, 175, 275]
        layer1 = list(np.linspace(0, 2 * np.pi, 6))
        layer2 = list(np.linspace(0, 2 * np.pi, 11))
        layer3 = list(np.linspace(0, 2 * np.pi, 16))

        for layer in layer1:
            r = distances_delta[0]
            phi = layer
            x, y = polar_to_cart(r, phi)
            x, y = move_cart_to_origin(x, y)
            sprites.append(arcade.Sprite(filename=self.texture,
                                         center_x=x,
                                         center_y=y,
                                         scale=0.5
                                         )
                           )


        for layer in layer2:
            r = distances_delta[1]
            phi = layer
            x, y = polar_to_cart(r, phi)
            x, y = move_cart_to_origin(x, y)
            sprites.append(arcade.Sprite(filename=self.texture,
                                         center_x=x,
                                         center_y=y,
                                         scale=0.5
                                         )
                           )



        for layer in layer3:
            r = distances_delta[2]
            phi = layer
            x, y = polar_to_cart(r, phi)
            x, y = move_cart_to_origin(x, y)
            sprites.append(arcade.Sprite(filename=self.texture,
                                         center_x=x,
                                         center_y=y,
                                         scale=0.5
                                         )
                           )



    def update_sprite(self, delta_time, sprite, vector):
        sprite.center_x, sprite.center_y = increase_angle(sprite.center_x, sprite.center_y,
                                                          self.speed * delta_time * vector)

    def animation_run(self, sprites, delta_time):
        vector = 1
        for sprite in zip(sprites, range(len(sprites))):
            if sprite[1] == 6:
                vector *= -1
            if sprite[1] == 17:
                vector *= -1

            self.update_sprite(delta_time, sprite[0], vector)
