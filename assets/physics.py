


from math import degrees
import arcade
import pymunk

from assets.MovementSprite import PhysicsSprite
from settings import FPS


class PhysicsSimulation:


    def __init__(self, window):
        
        self.window = window

        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0, 0)
        self.space.damping = 0.99

        self.sprites = None

        ### Game area
        self.g_lb = (20,20)
        self.g_lt = (20,self.window.height-20)
        self.g_rb = (self.window.width-20,20)
        self.g_rt = (self.window.width-20,self.window.height-20)

        static_lines = [
            pymunk.Segment(self.space.static_body, self.g_lb, self.g_lt, 10),
            pymunk.Segment(self.space.static_body, self.g_lt, self.g_rt, 10),
            pymunk.Segment(self.space.static_body, self.g_rt, self.g_rb, 10),
            pymunk.Segment(self.space.static_body, self.g_lb, self.g_rb, 10)
        ]
        for line in static_lines:
            line.elasticity = 1.0

        self.space.add(*static_lines)


    def set_sprites(self, sprites):

        self.sprites = sprites


    def update(self):

        if self.sprites is not None:

            self.space.step(1 / FPS)

            for sprite in self.sprites:

                sprite.center_x = sprite.shape.body.position.x
                sprite.center_y = sprite.shape.body.position.y
                sprite.angle = degrees(sprite.shape.body.angle)

                if (0 >= sprite.shape.body.position.x or sprite.shape.body.position.x >= self.window.width
                        or 0 >= sprite.shape.body.position.y or sprite.shape.body.position.y >= self.window.height
                ):
                    self.sprites.remove(sprite)


    def get_space(self):

        return self.space


    Space = property(get_space)