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

        # UIManager
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        layout = arcade.gui.UILayout(x= (self.window.width - self.window.width/1.5) / 2, width=self.window.width/1.5, height=80)

        box = arcade.gui.UIBoxLayout(vertical=False, space_between=SPACE_BETWEEN_BUTTONS)

        # gear
        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/gear.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/gear.png") 

        self.btn_gear = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        self.btn_gear.on_click = self.btn_gear_clicked
        box.add(self.btn_gear)


        # star_square
        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/star_square.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/star_square.png") 

        self.btn_star_square = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        # add event
        # self.btn_play.on_click = 
        box.add(self.btn_star_square)

        # play
        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/play.png") 

        self.btn_play = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        # add event
        self.btn_play.on_click = self.btn_play_clicked
        box.add(self.btn_play)

        # up
        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/up.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png") 

        self.btn_up = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        # add event
        # self.btn_play.on_click = 
        box.add(self.btn_up)

        # sound_on
        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png") 

        self.btn_sound_on = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        self.btn_sound_on.on_click = self.btn_sound_clicked
        box.add(self.btn_sound_on)


        layout.add(arcade.gui.UIAnchorWidget(child=box))

        bg_player = arcade.load_texture(os.path.join(ROOT_DIR, "resources/background_player.png"))

        self.ui_manager.add(arcade.gui.UITexturePane(child=layout,
                                                    tex = bg_player))
        
        # self.ui_manager.add(layout)
        
        self.section = VolumeSliderSection(layout.right - SPACE_BETWEEN_BUTTONS - SIZE_BUTTON / 2 + 6.5, self.btn_sound_on.top + 60, 10, 100)
        self.section.enabled=False
        self.section_manager.add_section(self.section)

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
        settingsView = SettingsView()
        self.window.show_view(settingsView)


class SettingsView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        
        hbox = arcade.gui.UIBoxLayout(vertical=False, space_between=200)

        vbox = arcade.gui.UIBoxLayout()
        vbox1 = arcade.gui.UIBoxLayout()

        text_area = arcade.gui.UITextArea(
            text="Настройки",
            font_size=26,
            text_color=arcade.color_from_hex_string("#000"),
            align="center"
            )
        
        vbox.add(text_area)

        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/close.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/close.png") 

        self.btn_close_view = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        self.btn_close_view.on_click = self.btn_close_clicked
        vbox1.add(self.btn_close_view)

        hbox.add(vbox)
        hbox.add(vbox1)

        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=hbox, anchor_y="top", align_y=-25))

        

        

    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.ui_manager.draw()


    def btn_close_clicked(self, *_):
        view = ContainerView()
        self.window.show_view(view)
    
    