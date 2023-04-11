import arcade
import math
import pymunk
from pymunk import Vec2d

class PhysicsSprite(arcade.Sprite):
    def __init__(self, space, position, mass, moment, body_type, direction = None, file_name=None, _texture=None, sprite_scale=1):
        super().__init__(filename=file_name, texture=_texture, scale=sprite_scale, center_x=position[0], center_y=position[1])
        
        body = pymunk.Body(mass, moment, body_type)
        body.position = Vec2d(*position)

        if direction is not None:
            body.apply_impulse_at_local_point(Vec2d(*direction))

            def constant_velocity(body, gravity, damping, dt):
                body.velocity = body.velocity.normalized() * 400

            body.velocity_func = constant_velocity

        self.shape = pymunk.Poly(body, self.get_hit_box())
        self.shape.elasticity = 1.0

        space.add(body, self.shape)


    def rotate(self, point, degrees: float, rot=True):

        if rot:
            self.shape.body.angle += degrees

        self.shape.body.position = arcade.rotate_point(
            self.shape.body.position.x, self.shape.body.position.y,
            point[0], point[1], degrees
        )


class TestWindow(arcade.Window):

    def __init__(self, width, height) -> None:
        super().__init__(width, height)

        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0, -900)
        self.space.damping = 0.99

        self.sprites = arcade.SpriteList()

        # 1
        position = (300, 300)
        size = 60
        direction = (10, 10)

        self.sprites.append(PhysicsSprite(self.space, position, 1, 
                                          pymunk.moment_for_box(1, (size, size)),
                                          pymunk.Body.DYNAMIC, _texture=arcade.make_soft_square_texture(size, (0, 255, 0), outer_alpha=255)))

        self.flipper = PhysicsSprite(self.space, (self.width//2, self.height//2), 1, 1, pymunk.Body.KINEMATIC, 
                                     _texture=arcade.make_soft_square_texture(90, (0,0,0, 200), outer_alpha=230))
        
        self.sprites.append(self.flipper)

        ### Game area
        self.g_lb = (20,20)
        self.g_lt = (20,self.height-20)
        self.g_rb = (self.width-20,20)
        self.g_rt = (self.width-20,self.height-20)

        static_lines = [
            pymunk.Segment(self.space.static_body, self.g_lb, self.g_lt, 3),
            pymunk.Segment(self.space.static_body, self.g_lt, self.g_rt, 3),
            pymunk.Segment(self.space.static_body, self.g_rt, self.g_rb, 3),
            pymunk.Segment(self.space.static_body, self.g_lb, self.g_rb, 3)
        ]
        for line in static_lines:
            line.elasticity = 1.0

        self.space.add(*static_lines)
    

    def update(self, delta_time):
        
        self.flipper.rotate((self.flipper.center_x, self.flipper.center_y), 3.14/100)

        self.space.step(1 / 60)

        for sprite in self.sprites:
            sprite.center_x = sprite.shape.body.position.x
            sprite.center_y = sprite.shape.body.position.y
            sprite.angle = math.degrees(sprite.shape.body.angle)


    def on_draw(self):
        
        arcade.draw_xywh_rectangle_filled(0, 0, self.width, self.height, (90,90,90))

        arcade.draw_line(*self.g_lb, *self.g_lt, (150,0,0,140), 3)
        arcade.draw_line(*self.g_lt, *self.g_rt, (150,0,0,140), 3)
        arcade.draw_line(*self.g_rt, *self.g_rb, (150,0,0,140), 3)
        arcade.draw_line(*self.g_lb, *self.g_rb, (150,0,0,140), 3)

        self.sprites.draw()


if __name__ == "__main__":

    window = TestWindow(600, 500)

    arcade.run()