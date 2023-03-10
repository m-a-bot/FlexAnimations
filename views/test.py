import arcade
import arcade.gui
from arcade.gui.widgets import _Rect


class TestView(arcade.View):

    def __init__(self):

        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.layout = arcade.gui.UILayout(0,0, self.window.width, self.window.height,
                                          size_hint=(1,1))
        
        self.player = arcade.gui.UIBoxLayout(vertical=False, space_between=self.layout.width/4)
        self.center_button = arcade.gui.UIBoxLayout(vertical=False, space_between=40)

        self.player.add(arcade.gui.UIFlatButton())
        self.player.add(self.center_button)
        self.player.add(arcade.gui.UIFlatButton())

        self.center_button.add(arcade.gui.UIFlatButton(width=50))
        self.center_button.add(arcade.gui.UIFlatButton(width=50))
        self.center_button.add(arcade.gui.UIFlatButton(width=50))

        self.layout.add(arcade.gui.UIAnchorWidget(child=self.player.with_border(),
                                                  anchor_y="bottom"))

        self.manager.add(self.layout.with_background(arcade.make_soft_square_texture(20, (200,200,145), outer_alpha=255)))


    def on_draw(self):
        
        self.clear()
        arcade.start_render()

        arcade.draw_xywh_rectangle_filled(0,0, self.window.width, self.window.height, (120, 120, 120, 200) )
        self.manager.draw()

    
    def on_resize(self, width: int, height: int):
        
        super().on_resize(width, height)

        self.layout._rect = _Rect(0,0,width, height)

        if width < 800:
            self.player._space_between=self.layout.width/8

        elif width > 1200:
            self.player._space_between=self.layout.width/3
        else:
            self.player._space_between=self.layout.width/4