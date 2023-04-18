from animations.animation import Animation

class Chaos(Animation):

    def __init__(self):
        
        self.simulation = None


    def animation_run(self, sprites, delta_time):

        if self.simulation is not None:
            self.simulation.update()