from typing import Optional
from settings import ROOT_DIR
from sections.volume_slider import VolumeSliderSection
import arcade
import arcade.gui
import arcade.gui.events
import os


SIZE_BUTTON = 40
SPACE_BETWEEN_BUTTONS = 60

class ContainerView(arcade.View):

    def __init__(self):

        super().__init__()

        self.paused = False
        self.sound_off = False

        self.setup()

    
    def setup(self):

        # UIManager
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        
        self.main_layout = arcade.gui.UILayout(0,0, self.window.width, self.window.height,
                                          size_hint=(1,1),
                                          size_hint_min=(800, 600),
                                          size_hint_max=(1600, 900))
        
        player_layout = arcade.gui.UILayout(0,0, self.window.width, 80, 
                                            size_hint=(1,0),
                                            size_hint_min=(800, 60),
                                            size_hint_max=(1600, 90))

        self.main_box = arcade.gui.UIBoxLayout(vertical=False, space_between=self.window.width//3 - 60, 
                                               size_hint=(1,1))

        # gear
        self.btn_gear = self.add_texture_button(
            ":resources:onscreen_controls/flat_dark/gear.png",
            ":resources:onscreen_controls/shaded_dark/gear.png",
        )
        self.btn_gear.on_click = self.btn_gear_clicked
        self.main_box.add(arcade.gui.UIWrapper(child=self.btn_gear, padding=(20, 0, 20, 0)))


        self.center_box = arcade.gui.UIBoxLayout(vertical=False, space_between=60,
                                                 size_hint=(1,1))
        # star_square
        self.main_box.add(self.center_box)

        self.btn_star_square = self.add_texture_button(
            ":resources:onscreen_controls/flat_dark/star_square.png",
            ":resources:onscreen_controls/shaded_dark/star_square.png",
        )
        # add event
        # self.btn_play.on_click = 
        self.center_box.add(self.btn_star_square)


        # play
        self.btn_play = self.add_texture_button(
            ":resources:onscreen_controls/flat_dark/play.png",
            ":resources:onscreen_controls/shaded_dark/play.png" ,
        )
        # add event
        self.btn_play.on_click = self.btn_play_clicked
        self.center_box.add(self.btn_play)


        # up
        self.btn_up = self.add_texture_button(
            ":resources:onscreen_controls/flat_dark/up.png",
        ":resources:onscreen_controls/shaded_dark/up.png",
        )
        # add event
        # self.btn_play.on_click = 
        self.center_box.add(self.btn_up)


        # sound_on
        self.btn_sound_on = self.add_texture_button(
            ":resources:onscreen_controls/flat_dark/sound_on.png",
        ":resources:onscreen_controls/shaded_dark/sound_on.png",
        )
        self.btn_sound_on.on_click = self.btn_sound_clicked
        self.main_box.add(arcade.gui.UIWrapper(child=self.btn_sound_on, padding=(20,0,20,0)))


        player_layout.add(arcade.gui.UIAnchorWidget(child=self.main_box, anchor_y="bottom"))        

        bg_player = arcade.make_soft_square_texture(128, arcade.color_from_hex_string("#d1cfcf"), outer_alpha=255)

        self.main_layout.add(arcade.gui.UITexturePane(child=player_layout,
                                                    tex = bg_player, 
                                                    padding=(20,20,20,20)))
        self.ui_manager.add(self.main_layout)
        
        # self.ui_manager.add(layout)
        
        # self.section = VolumeSliderSection(layout.right - SPACE_BETWEEN_BUTTONS - SIZE_BUTTON / 2 + 6.5, self.btn_sound_on.top + 60, 10, 100)
        # self.section.enabled=False
        # self.section_manager.add_section(self.section)

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)


    def add_texture_button(self, texture_name, texture_shared, scale=1):

        __texture = arcade.load_texture(texture_name)
        __texture_shared = arcade.load_texture(texture_shared) 

        return arcade.gui.UITextureButton(
            texture = __texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
            scale = scale
        )


    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#BABAB4"))


    def on_draw(self):
        self.clear()
        arcade.start_render()
        # arcade.draw_xywh_rectangle_filled(self.window.width//6, 0, self.window.width//1.5, 80, arcade.color_from_hex_string("#E1DFDF"))
        self.ui_manager.draw()

    
    def btn_play_clicked(self, *_):
        
        if self.paused:
            self.set_play()
            self.paused = False
        else:
            self.set_pause()
            self.paused = True

    def btn_gear_clicked(self, *_):
        ...

    def btn_sound_clicked(self, *_):
        
        if self.sound_off:
            self.section.enabled=False
            self.set_sound_on()
            self.sound_off = False
        else:
            self.section.enabled=True
            self.set_sound_off()
            self.sound_off = True


    def set_pause(self):
        self.btn_play.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/pause_square.png")
        self.btn_play.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/pause_square.png")
        self.btn_play.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/pause_square.png")
        
    def set_play(self):
        self.btn_play.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/play.png")
        self.btn_play.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        self.btn_play.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/play.png")
        
    def set_sound_on(self):
        self.btn_sound_on.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")
        self.btn_sound_on.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")
        self.btn_sound_on.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")
        
    def set_sound_off(self):
        self.btn_sound_on.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")
        self.btn_sound_on.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_off.png")
        self.btn_sound_on.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")

    def btn_gear_clicked(self, *_):
        # settingsView = SettingsView()
        # self.window.show_view(settingsView)
        ...




    
    