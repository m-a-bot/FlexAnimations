import random
import numpy
import pymunk
from animations.animation import Animation, FiguresType
from assets.MovementSprite import PhysicsSprite
from assets.physics import PhysicsSimulation
from settings import HEIGHT, WIDTH

class Chaos(Animation):

    def __init__(self, figure_type, music_track):

        super().__init__(figure_type, music_track)
        
        self.simulation = None
        self.speed = 1100

        if figure_type == FiguresType.CIRCLE:
            self.texture = "resources/icons/Круг.png"
        if figure_type == FiguresType.TRIANGLE:
            self.texture = "resources/icons/Треугольник.png"
        if figure_type == FiguresType.SQUARE:
            self.texture = "resources/icons/Квадрат.png"
        self.texture = 'resources/icons/current_figure.png'

        self.angles = [x for x in range(-360, 360, 25) if x != 0]

    def fill_sprites(self, sprites):

        ## add sprites
        mass = 100
        elasticity = 0.4
        dynamic = pymunk.Body.DYNAMIC
        kynematic = pymunk.Body.KINEMATIC
        shift = 50
        scale = 1
        if len(sprites) > 0:
            if isinstance(sprites[0], PhysicsSprite):
                for sprite in sprites:
                    sprite.remove_from_space(PhysicsSimulation.get_space())

        super().fill_sprites(sprites)

        for cur_x in range(0, WIDTH, WIDTH // 8):
            for _ in range(3):
                position = (random.randint(shift, WIDTH-shift), random.randint(shift, HEIGHT-shift))
                direction = (numpy.sin(numpy.radians(random.choice(self.angles))), numpy.cos(numpy.radians(random.choice(self.angles))))

                sprites.append(PhysicsSprite(PhysicsSimulation.get_space(), position, mass, dynamic, elasticity, direction, file_name=self.texture, sprite_scale=scale))


    def animation_run(self, sprites, delta_time):
        if self.music_track.piece_of_points is not None:
            koef_1 = 1
            try:
                koef_1 = self.music_track.piece_of_points[len(self.music_track.piece_of_points) // 2] + 0.05
                # print(koef_1)
            except:
                ...
            # koef_2 = sum(self.music_track.piece_of_points) / len(self.music_track.piece_of_points)
            if not 0.6 <= koef_1 < 0.9:
                for sprite in sprites:
                    sprite.change_velocity(koef_1 * self.speed)

        PhysicsSimulation.update(sprites)
