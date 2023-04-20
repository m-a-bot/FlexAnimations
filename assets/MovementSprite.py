import arcade
import math
import pymunk
from pymunk import Vec2d

class PhysicsSprite(arcade.Sprite):
    def __init__(self, space, position, mass, body_type, elasticity = 1.0, direction = None, constant_speed=400, file_name=None, _texture=None, sprite_scale=1):
        super().__init__(filename=file_name, texture=_texture, scale=sprite_scale, center_x=position[0], center_y=position[1])
        
        moment = pymunk.moment_for_poly(mass, self.get_hit_box())
        
        self.speed = 300
        self.body = pymunk.Body(mass, moment, body_type)
        self.body.position = Vec2d(*position)
        self.body.velocity = Vec2d(direction[0]*self.speed, direction[1]*self.speed)

        def constant_velocity(body, gravity, damping, dt):
                body.velocity = body.velocity.normalized() * self.speed

        
        def limit_velocity(body, gravity, damping, dt):
            max_velocity = 600
            pymunk.Body.update_velocity(body, gravity, damping, dt)
            l = body.velocity.length
            if l > max_velocity:
                scale = max_velocity / l
                body.velocity = body.velocity * scale

            if l < self.speed:
                body.velocity = body.velocity.normalized() * self.speed

        self.body.velocity_func = limit_velocity

        # if direction is not None:
        #     self.body.apply_impulse_at_local_point(direction)

        #     self.body.velocity_func = constant_velocity

        self.shape = pymunk.Poly(self.body, self.get_hit_box())
        self.shape.elasticity = elasticity

        space.add(self.body, self.shape)


    def remove_from_space(self, space):
         
         space.remove(self.body, self.shape)


    def rotate(self, point, degrees: float, rot=True):

        if rot:
            self.shape.body.angle += degrees

        self.shape.body.position = arcade.rotate_point(
            self.shape.body.position.x, self.shape.body.position.y,
            point[0], point[1], degrees
        )