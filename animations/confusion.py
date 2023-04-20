import random
import pymunk
from animations.animation import Animation, FiguresType
from assets.MovementSprite import PhysicsSprite
from assets.physics import PhysicsSimulation
from settings import HEIGHT, WIDTH

class Chaos(Animation):

    def __init__(self, figure_type):
        
        self.simulation = None

        if figure_type == FiguresType.CIRCLE:
            self.texture = "resources/icons/Круг.png"
        if figure_type == FiguresType.TRIANGLE:
            self.texture = "resources/icons/Треугольник.png"
        if figure_type == FiguresType.SQUARE:
            self.texture = "resources/icons/Квадрат.png"

    def fill_sprites(self, sprites):

        ## add sprites
        mass = 1
        elasticity = 0.9
        dynamic = pymunk.Body.DYNAMIC
        kynematic = pymunk.Body.KINEMATIC
        shift = 50
        scale = 0.9

        if isinstance(sprites, PhysicsSprite):
            for sprite in sprites:
                sprite.remove_from_space(PhysicsSimulation.get_space())

        super().fill_sprites(sprites)

        for cur_x in range(0, WIDTH, WIDTH // 8):
            for _ in range(3):
                position = (random.randint(shift, WIDTH-shift), random.randint(shift, HEIGHT-shift))
                direction = (random.choice([-1, 1]),random.choice([-1, 1]))

                sprites.append(PhysicsSprite(PhysicsSimulation.get_space(), position, mass, dynamic, elasticity, direction, file_name=self.texture, sprite_scale=scale))


    def animation_run(self, sprites, delta_time):

        PhysicsSimulation.update(sprites)
