import arcade
from animations.animation import Animation
from settings import *
from functools import partial
import math


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


def move(x, y, inc, a, b, c, d):

    x, y = x + inc, a + b * math.sin(c * x + d)

    return x, y


class Wave(Animation):
    def __init__(self):
        super().__init__()
        self.speed = 40
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 4
        self.center = (self.center_x, self.center_y)

        self.a = 360
        self.b = 100
        self.c = 0.05
        self.d = - WIDTH / 2
        self.sprite_width = 100

    def fill_sprites(self, sprites):
        super().fill_sprites(sprites)
        sprites.append(arcade.Sprite(filename=":resources:gui_basic_assets/red_button_press.png",
                                     center_x=self.center_x,
                                     center_y=self.center_y,
                                     scale=1))

    def update_sprite(self, delta_time, sprite):
        if sprite.center_x > WIDTH + self.sprite_width:
            sprite.center_x = - self.sprite_width
        sprite.center_x, sprite.center_y = move(sprite.center_x, sprite.center_y,
                                                delta_time * self.speed, self.a, self.b, self.c, self.d)

    def animation_run(self, sprites, delta_time):
        for sprite in sprites:
            self.update_sprite(delta_time, sprite)
