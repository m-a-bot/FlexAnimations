import arcade
import arcade.color

class VolumeSliderSection(arcade.Section):

    def __init__(self, left: int, bottom: int, width: int, height: int):
        super().__init__(left, bottom, width, height)

    def on_draw(self):
        
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top,
                                          self.bottom, arcade.color_from_hex_string("#000"))
        
        arcade.draw_lrtb_rectangle_filled(self.left + self.width/2 - 3, self.right - self.width/2 + 3, self.top - 3,
                                          self.bottom + 3, arcade.color_from_hex_string("#fff"))