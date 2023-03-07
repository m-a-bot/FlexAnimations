import arcade
from assets.circle import SimpleCircle 

class CanvasSection(arcade.Section):

    def __init__(self, left, bottom, width, height):
        super().__init__(left, bottom, width, height)

        self.circle = SimpleCircle(20, arcade.color.ANTIQUE_RUBY)

        self.circle.set_position(width/2, height/2) 

    def on_update(self, delta_time: float):
        
        self.circle.update()


    def on_draw(self):
        
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top,
                                          self.bottom, arcade.color_from_hex_string("#abc977"))
        
        self.circle.draw()