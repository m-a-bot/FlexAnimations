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
    def __init__(self, figure_type, music_track):
        self.figure_type = figure_type
        self.music_track = music_track
    def fill_sprites(self, sprites):
        sprites.clear()

    def animation_run(self, sprites, delta_time):
        pass
