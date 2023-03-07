import arcade
from scripts.SoundPlayer import SoundPlayer


COLOR1 = arcade.color_from_hex_string("#E1DFDF")

SIZE_BUTTON = 40

class PlayerSection(arcade.Section):
    
    def __init__(self, left, bottom, width, height):

        super().__init__(left, bottom, width, height)

        self.__player = SoundPlayer(r"resources/music/sample-6s.wav")
        self.music_play = False

        self.play = arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")

        self.pause = arcade.load_texture(":resources:onscreen_controls/flat_dark/pause_square.png")

        self.up = arcade.load_texture(":resources:onscreen_controls/flat_dark/up.png")

        self.star_square = arcade.load_texture(":resources:onscreen_controls/flat_dark/star_square.png")

        self.gear = arcade.load_texture(":resources:onscreen_controls/flat_dark/gear.png")

        self.sound_on = arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")


    def on_draw(self):
        
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top,
                                          self.bottom, COLOR1)
        
        arcade.draw_lrwh_rectangle_textured((self.left + self.right) / 2 - SIZE_BUTTON/2, self.bottom + self.height/2 - SIZE_BUTTON/2, 
                SIZE_BUTTON, SIZE_BUTTON, self.play)

        arcade.draw_lrwh_rectangle_textured((self.left + self.right) / 2 + 60 - SIZE_BUTTON/2, self.bottom + self.height/2 - SIZE_BUTTON/2, 
                SIZE_BUTTON, SIZE_BUTTON, self.up)

        arcade.draw_lrwh_rectangle_textured((self.left + self.right) / 2 - 60 - SIZE_BUTTON/2, self.bottom + self.height/2 - SIZE_BUTTON/2, 
                SIZE_BUTTON, SIZE_BUTTON, self.star_square)

        arcade.draw_lrwh_rectangle_textured(20, self.bottom + self.height/2 - SIZE_BUTTON/2, 
                SIZE_BUTTON, SIZE_BUTTON, self.gear)  

        arcade.draw_lrwh_rectangle_textured(self.right - 60, self.bottom + self.height/2 - SIZE_BUTTON/2, 
                SIZE_BUTTON, SIZE_BUTTON, self.sound_on)                                          

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        if self.music_play:
                self.__player.stop()
                self.music_play = False
        else:
                self.__player.play()
                self.music_play = True