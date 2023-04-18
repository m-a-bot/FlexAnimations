from enum import Enum

class AnimationMode(Enum):
    TORNADO = 1
    WAVE = 2
    CHAOS = 3

class FiguresType(Enum):
    CIRCLE = 1
    TRIANGLE = 2
    SQUARE = 3

class Animation():
    figure_type = None
    def __init__(self, figure_type):
        self.figure_type = figure_type
    def fill_sprites(self, sprites):
        sprites.clear()

    def animation_run(self, sprites, delta_time):
        pass
