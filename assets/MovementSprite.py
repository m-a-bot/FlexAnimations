import arcade
import math
import pymunk
from pymunk import Vec2d

class PhysicsSprite(arcade.Sprite):
    def __init__(self, space, position, mass, body_type, elasticity = 1.0, direction = None, constant_speed=400, file_name=None, _texture=None, sprite_scale=1):
        super().__init__(filename=file_name, texture=_texture, scale=sprite_scale, center_x=position[0], center_y=position[1])
        
        moment = pymunk.moment_for_poly(mass, self.get_hit_box())
        body = pymunk.Body(mass, moment, body_type)
        body.position = Vec2d(*position)

        def constant_velocity(body, gravity, damping, dt):
                body.velocity = body.velocity.normalized() * constant_speed

        if direction is not None:
            body.apply_impulse_at_local_point(direction)

            body.velocity_func = constant_velocity

        self.shape = pymunk.Poly(body, self.get_hit_box())
        self.shape.elasticity = elasticity

        space.add(body, self.shape)


    def rotate(self, point, degrees: float, rot=True):

        if rot:
            self.shape.body.angle += degrees

        self.shape.body.position = arcade.rotate_point(
            self.shape.body.position.x, self.shape.body.position.y,
            point[0], point[1], degrees
        )