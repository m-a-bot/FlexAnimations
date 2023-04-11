import arcade
import math
import pymunk
from pymunk import Vec2d



class TestWindow(arcade.Window):

    class PhysicsSprite(arcade.Sprite):
        def __init__(self, pymunk_shape, file_name=None, _texture=None, sprite_scale=1):
            super().__init__(filename=file_name, texture=_texture, scale=sprite_scale, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
            self.shape = pymunk_shape

    def __init__(self, width, height) -> None:
        super().__init__(width, height)

        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0, 0)
        self.space.damping = 0.99

        self.sprites = arcade.SpriteList()

        # 1
        position = (300, 300)
        size = 60
        direction = (10, 10)

        body = pymunk.Body(1, pymunk.moment_for_box(1, (size, size)))
        body.position = Vec2d(*position)
        body.apply_impulse_at_local_point(Vec2d(*direction))

        shape = pymunk.Poly.create_box(body, (size, size))
        shape.elasticity = 1.0

        def constant_velocity(body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * 400

        body.velocity_func = constant_velocity
        self.space.add(body, shape)

        self.sprites.append(TestWindow.PhysicsSprite(shape, _texture=arcade.make_soft_square_texture(size, (0, 255, 0), outer_alpha=255)))

        body = pymunk.Body(1, pymunk.moment_for_box(1, (size, size)))
        body.position = Vec2d(350, 200)
        body.apply_impulse_at_local_point(Vec2d(-10, 10))

        shape = pymunk.Poly.create_box(body, (size, size))
        shape.elasticity = 1.0

        def constant_velocity1(body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * 300

        body.velocity_func = constant_velocity1
        self.space.add(body, shape)

        self.sprites.append(TestWindow.PhysicsSprite(shape, _texture=arcade.make_soft_square_texture(size, (0, 0, 255), outer_alpha=255)))


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
        
        #self.sprites[1].shape.body.apply_impulse_at_local_point(Vec2d(5, -5))

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