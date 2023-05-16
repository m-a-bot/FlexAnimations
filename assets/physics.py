


from math import degrees
import arcade
import pymunk

from assets.MovementSprite import PhysicsSprite
from settings import FPS, HEIGHT, WIDTH


class PhysicsSimulation:

    __space = pymunk.Space()
    __space.gravity = pymunk.Vec2d(0, 0)
    __space.damping = 0.99

    ### Game area
    g_lb = (20,20)
    g_lt = (20,HEIGHT-20)
    g_rb = (WIDTH-20,20)
    g_rt = (WIDTH-20,HEIGHT-20)

    line_size = 10
    static_lines = [
        pymunk.Segment(__space.static_body, g_lb, g_lt, line_size),
        pymunk.Segment(__space.static_body, g_lt, g_rt, line_size),
        pymunk.Segment(__space.static_body, g_rt, g_rb, line_size),
        pymunk.Segment(__space.static_body, g_lb, g_rb, line_size)
    ]
    for line in static_lines:
        line.elasticity = 1.0

    __space.add(*static_lines)


    @staticmethod
    def update(sprites):

        if sprites is not None:
            PhysicsSimulation.__space.step(1 / FPS)

            for sprite in sprites:

                sprite.center_x = sprite.shape.body.position.x
                sprite.center_y = sprite.shape.body.position.y
                sprite.angle = degrees(sprite.shape.body.angle)

                if (0 >= sprite.shape.body.position.x or sprite.shape.body.position.x >= WIDTH
                        or 0 >= sprite.shape.body.position.y or sprite.shape.body.position.y >= HEIGHT
                ):
                    sprites.remove(sprite)


    @staticmethod
    def get_space():

        return PhysicsSimulation.__space
