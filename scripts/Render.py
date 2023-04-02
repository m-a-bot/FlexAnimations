import arcade
import pymunk as pm

collision_types = {
    "" : 1,
    "" : 2,
}


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename, sprite_scale=1):
        super().__init__(filename, scale=sprite_scale, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.shape = pymunk_shape




