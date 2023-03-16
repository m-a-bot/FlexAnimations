import arcade
import numpy as np

# TODO
"""
Использовать ряды Фурье
1сек = 44100 эл.
1/60 сек = 735 эл.
735 = 49 * 15
"""
# TODO
# Переименовать self.current_song_index
class MusicTrack(arcade.Section):

    def __init__(self, left: int, bottom: int, width: int, height: int):
        super().__init__(left, bottom, width, height)

        self.music_data = None

        self.current_song_index = 0

        self.points = []

        self.x = np.linspace(self.left, self.right, 49 * 2)


    def update(self, delta_time):
        
        self.points.clear()

        if self.music_data is not None:
            s = 0
            i = 0

            try:
                single_frame_data = self.music_data[self.current_song_index * 735: (self.current_song_index+2) * 735]

                for x in single_frame_data:
                    s += x
                    i += 1
                    if i == 15:
                        self.points.append(s / i)
                        s = 0
                        i = 0

                A = min(self.points)
                B = max(self.points)

                for i, x in enumerate(self.points):
                    self.points[i] = (x - A) / (B - A)
            
            except:
                ...


    def on_draw(self):
        
        arcade.draw_xywh_rectangle_filled(self.left, self.bottom, self.width, self.height, (255,255,255, 30))

        if self.music_data is not None:
            try:
                points_left = []
                points_right = []
                i = 0
                while i < 49:

                    points_left.append([self.x[i], self.bottom + self.points[i] * self.height])
                    i += 1

                while i < 49*2:

                    points_right.append([self.x[i], self.bottom + self.points[i] * self.height])
                    i += 1
                    
                arcade.draw_line_strip(points_left, (190,0,0), line_width=5)
                arcade.draw_line(*points_left[-1], *points_right[0], (190, 0,0), line_width=5)
                arcade.draw_line_strip(points_right, (0,0,0, 159), line_width=5)
            except:
                ...

