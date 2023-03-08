import arcade

class CanvasSection(arcade.Section):

    def on_draw(self):
        
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top,
                                          self.bottom, arcade.color_from_hex_string("#abc977"))