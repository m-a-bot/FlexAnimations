from typing import Optional
import arcade
import numpy.random
from settings import WIDTH, HEIGHT

class MovementSprite(arcade.Sprite):

    def __init__(self, delta_x=0, delta_y=0, barriers = None, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: arcade.Texture = None, angle: float = 0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)

        self.delta_x = delta_x
        self.delta_y = delta_y
        self.barriers = barriers

        self.rotation_angle = numpy.random.choice([-2,-1,1,2])


    # @staticmethod
    # @property
    # def set_window_width(value):
    #     MovementSprite.width = value

    
    # @staticmethod
    # @property
    # def set_window_height(value):
    #     MovementSprite.height = value


    def move(self):
        self.center_x += self.delta_x
        self.center_y += self.delta_y
        
        radius = self.collision_radius // 2
        self.angle += self.rotation_angle

        if self.center_x - radius < 0 and self.delta_x < 0:
            self.delta_x *= -1
        if self.center_y - radius < 0 and self.delta_y < 0:
            self.delta_y *= -1
        if self.center_x + radius > WIDTH and self.delta_x > 0:
            self.delta_x *= -1
        if self.center_y + radius > HEIGHT and self.delta_y > 0:
            self.delta_y *= -1

        # print(MovementSprite.width, MovementSprite.height)


    def update(self):
        self.move()