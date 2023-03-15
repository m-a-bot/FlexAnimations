import arcade
import arcade.color

class VolumeSliderSection(arcade.Section):

    def __init__(self, left: int, bottom: int, width: int, height: int, volume_level):
        super().__init__(left, bottom, width, height)

        self.volume_level = volume_level

    def on_draw(self):
        
        arcade.draw_lrtb_rectangle_filled(self.width*.968-self.width//100, self.width*.968+self.width//100, self.height//4, self.height//8+self.height//225, arcade.color.GRAY)
        arcade.draw_line(self.width*.968, self.height//7, self.width*.968, self.height//4-self.height//65, arcade.color.WHITE, line_width = 5)
        arcade.draw_line(self.width*.968-self.width//150,self.height//7+self.volume_level, self.width*.968+self.width//150,self.height//7+self.volume_level, arcade.color.WHITE, line_width = 5)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.sound_bar_is_visible:
                if y > self.height//7 and y < self.height//4 - self.height//65:
                    if x > self.width*.968-self.width//125 and x < self.width*.968+self.width//125:
                        self.volume_level = y-self.height//7
                        if self.media_player:
                            self.media_player.volume = self.volume_level/100