from math import degrees
import random

import arcade
import unittest

import pymunk
from pymunk import Vec2d

from assets.MovementSprite import PhysicsSprite
from assets.scripts.Render import get_rectangle_gradient, get_triangle_random, get_custom_circle
from settings import FPS


class FakeWindow:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        ### Physics

        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0, 0)
        self.space.damping = 0.99

        self.sprites = arcade.SpriteList()

        for _ in range(3):
            self.sprites.append(
                PhysicsSprite(self.space, (random.randint(50, self.width - 50), random.randint(50, self.height - 50)),
                              10, pymunk.Body.DYNAMIC, elasticity=0.9,
                              direction=(random.choice([-10, 10]), random.choice([-10, 10])),
                              _texture=arcade.make_circle_texture(50, (255, 0, 0)), sprite_scale=1.3))

        for _ in range(2):
            self.sprites.append(
                PhysicsSprite(self.space, (random.randint(50, self.width - 50), random.randint(50, self.height - 50)),
                              1, pymunk.Body.DYNAMIC, elasticity=0.9,
                              direction=(random.choice([-10, 10]), random.choice([-10, 10])),
                              _texture=arcade.make_soft_square_texture(40, (0, 0, 255), outer_alpha=255),
                              sprite_scale=0.9))

        r_grad = arcade.Texture("rect_grad", image=get_rectangle_gradient(120, 120, (120, 120, 9), (255, 45, 129)))
        triangle1 = arcade.Texture("triangle1", image=get_triangle_random(90, 100))

        for _ in range(4):
            self.sprites.append(
                PhysicsSprite(self.space, (random.randint(50, self.width - 50), random.randint(50, self.height - 50)),
                              1, pymunk.Body.DYNAMIC, elasticity=0.8,
                              direction=(random.choice([-10, 10]), random.choice([-10, 10])),
                              _texture=r_grad, sprite_scale=1))

        for _ in range(2):
            self.sprites.append(
                PhysicsSprite(self.space, (random.randint(50, self.width - 50), random.randint(50, self.height - 50)),
                              1, pymunk.Body.DYNAMIC, elasticity=0.8,
                              direction=(random.choice([-10, 10]), random.choice([-10, 10])),
                              _texture=triangle1, sprite_scale=1))

        circle = arcade.Texture("circle", image=get_custom_circle(100, 100, (57, 0, 23), (180, 0, 217)))
        for _ in range(5):
            self.sprites.append(
                PhysicsSprite(self.space, (random.randint(50, self.width - 50), random.randint(50, self.height - 50)),
                              10, pymunk.Body.DYNAMIC, elasticity=0.8,
                              direction=(random.choice([-10, 10]), random.choice([-10, 10])),
                              _texture=circle, sprite_scale=1))

            ### Game area
            self.g_lb = (20, 20)
            self.g_lt = (20, self.height - 20)
            self.g_rb = (self.width - 20, 20)
            self.g_rt = (self.width - 20, self.height - 20)

            static_lines = [
                pymunk.Segment(self.space.static_body, self.g_lb, self.g_lt, 3),
                pymunk.Segment(self.space.static_body, self.g_lt, self.g_rt, 3),
                pymunk.Segment(self.space.static_body, self.g_rt, self.g_rb, 3),
                pymunk.Segment(self.space.static_body, self.g_lb, self.g_rb, 3)
            ]
            for line in static_lines:
                line.elasticity = 1.0

            self.space.add(*static_lines)

    def update(self):
        self.space.step(1 / FPS)

        for sprite in self.sprites:

            sprite.center_x = sprite.shape.body.position.x
            sprite.center_y = sprite.shape.body.position.y
            sprite.angle = degrees(sprite.shape.body.angle)

            if (0 >= sprite.shape.body.position.x or sprite.shape.body.position.x >= self.width
                    or 0 >= sprite.shape.body.position.y or sprite.shape.body.position.y >= self.height
            ):
                self.sprites.remove(sprite)

    def on_draw(self):
        ...


class MyFiguresCase(unittest.TestCase):

    """
    Тест проверки принадлежности фигур области окна, то есть 2/3 фигур не должны покинуть эту область.
    Фигура удаляется из списка sprites, если покидает область экрана.
    10000 кадров. FPS = 24 кадра
    416,6 сек = 6 мин 56 сек
    """
    def test_disappearing_figures(self):
        WIDTH = 1280
        HEIGHT = 720
        view = FakeWindow(WIDTH, HEIGHT)

        for _ in range(10000):
            view.update()
            view.on_draw()

        expected = 16
        result = len(view.sprites)
        self.assertLessEqual(expected - result, expected // 3)


if __name__ == '__main__':
    unittest.main()
