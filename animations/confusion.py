import random
import pymunk
from animations.animation import Animation, FiguresType
from assets.MovementSprite import PhysicsSprite
from assets.physics import PhysicsSimulation
from settings import HEIGHT, WIDTH

class Chaos(Animation):

    def __init__(self, figure_type, music_track):

        super().__init__(figure_type, music_track)
        
        self.simulation = None
        self.speed = 800

        if figure_type == FiguresType.CIRCLE:
            self.texture = "resources/icons/Круг.png"
        if figure_type == FiguresType.TRIANGLE:
            self.texture = "resources/icons/Треугольник.png"
        if figure_type == FiguresType.SQUARE:
            self.texture = "resources/icons/Квадрат.png"
        self.texture = 'resources/icons/current_figure.png'

    def fill_sprites(self, sprites):

        ## add sprites
        mass = 1
        elasticity = 0.4
        dynamic = pymunk.Body.DYNAMIC
        kynematic = pymunk.Body.KINEMATIC
        shift = 50
        scale = 0.5
        if len(sprites) > 0:
            if isinstance(sprites[0], PhysicsSprite):
                for sprite in sprites:
                    sprite.remove_from_space(PhysicsSimulation.get_space())

        super().fill_sprites(sprites)

        for cur_x in range(0, WIDTH, WIDTH // 8):
            for _ in range(3):
                position = (random.randint(shift, WIDTH-shift), random.randint(shift, HEIGHT-shift))
                direction = (random.choice([-1, 1]),random.choice([-1, 1]))

                sprites.append(PhysicsSprite(PhysicsSimulation.get_space(), position, mass, dynamic, elasticity, direction, file_name=self.texture, sprite_scale=scale))


    def animation_run(self, sprites, delta_time):
        if self.music_track.piece_of_points is not None:
            koef_1 = self.music_track.piece_of_points[len(self.music_track.piece_of_points) // 2]
            # koef_2 = sum(self.music_track.piece_of_points) / len(self.music_track.piece_of_points)
            for sprite in sprites:
                sprite.change_velocity(self.speed * koef_1)

        PhysicsSimulation.update(sprites)
