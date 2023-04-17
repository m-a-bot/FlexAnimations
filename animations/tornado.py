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

class Tornado(Animation):
    def __init__(self):
        super().__init__()
        self.speed = 10
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 4
        self.center = (self.center_x, self.center_y)
    def fill_sprites(self, sprites):
        super().fill_sprites(sprites)
        sprites.append(arcade.Sprite(filename=":resources:gui_basic_assets/red_button_press.png",
                                     center_x=self.center_x,
                                     center_y=self.center_y,
                                     scale=1)
                      )

    def update_sprite(self, delta_time, sprite):
        sprite.center_x, sprite.center_y = increase_angle(sprite.center_x, sprite.center_y, delta_time * self.speed)


    def animation_run(self, sprites, delta_time):
        # print(1)
        # map(partial(self.update_sprite, delta_time), sprites)

        for sprite in sprites:
            self.update_sprite(delta_time, sprite)

        pass


