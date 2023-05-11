import arcade
from animations.animation import Animation
from settings import *
import math
from animations.animation import FiguresType


def move(x, number, inc, a, b, c, d, rng):
    x, y = x + inc, a + b * math.sin(c * x + d)

    if number == 0:
        y -= rng
        number = 1
    elif number == 2:
        y += rng
        number = 0
    else:
        number = 2

    return x, y, number


class Wave(Animation):
    def __init__(self, figure_type, music_track):
        super().__init__(figure_type, music_track)
        self.speed = 80
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 4
        self.center = (self.center_x, self.center_y)

        if figure_type == FiguresType.CIRCLE:
            self.texture = "resources/icons/Круг.png"
        if figure_type == FiguresType.TRIANGLE:
            self.texture = "resources/icons/Треугольник.png"
        if figure_type == FiguresType.SQUARE:
            self.texture = "resources/icons/Квадрат.png"

        self.a = 400
        self.b = 100
        self.c = 0.05
        self.d = - WIDTH // 2
        self.out_of_screen = WIDTH // 8

        self.number = 0
        self.rng = 150

    def fill_sprites(self, sprites):

        super().fill_sprites(sprites)

        for cur_x in range(0, WIDTH + self.out_of_screen * 2, WIDTH // 8):
            for _ in range(3):
                cur_y, self.number = move(cur_x, self.number, 0, self.a, self.b, self.c, self.d, self.rng)[1:]
                sprite = arcade.Sprite(filename=self.texture,
                                             center_x=cur_x,
                                             center_y=cur_y,
                                             scale=0.9)
                sprite.koef = 1
                sprite.prev = math.sin(self.c * sprite.center_x + self.d)
                sprites.append(sprite)

    def update_sprite(self, delta_time, sprite):

        if sprite.center_x >= WIDTH + self.out_of_screen:
            sprite.center_x = - self.out_of_screen
        sprite.center_x, sprite.center_y, self.number = move(sprite.center_x, self.number, delta_time * self.speed,
                                                             self.a,
                                                             self.b * sprite.koef,
                                                             self.c,
                                                             self.d, self.rng)

        sprite_cur = math.sin(self.c * sprite.center_x + self.d)

        if sprite_cur * sprite.prev <= 0:
            sprite.koef = (sum(self.music_track.points) / len(self.music_track.points) - 0.3) * 7
            # sprite.koef = min(self.music_track.points)
            # sprite.koef = sum(self.music_track.points) / len(self.music_track.points)
            # sprite.koef = (self.music_track.music_data[self.music_track.current_song_index] - 100) / 20
            # print(sprite.koef)

        sprite.prev = sprite_cur

    def animation_run(self, sprites, delta_time):
        for sprite in sprites:
            self.update_sprite(delta_time, sprite)
