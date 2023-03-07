import arcade
import numpy

class SimpleCircle(arcade.SpriteCircle):
    
    def update(self):

        # Convert angle in degrees to radians.
        angle_rad = numpy.radians(self.angle)

        # Rotate the ship
        self.angle += 30

        self.center_x += numpy.sin(angle_rad)
        self.center_y += numpy.cos(angle_rad)