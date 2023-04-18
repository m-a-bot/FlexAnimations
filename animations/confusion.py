from math import degrees
import random
import arcade
import pymunk
from animations.animation import Animation
from pymunk import Vec2d

from assets.MovementSprite import PhysicsSprite
from assets.scripts.Render import get_custom_circle, get_rectangle_gradient, get_triangle_random
from settings import FPS
from assets.physics import PhysicsSimulation

class Chaos(Animation):

    def __init__(self):
        
        self.simulation = None


    def animation_run(self, sprites, delta_time):

        if self.simulation is not None:
            self.simulation.update()