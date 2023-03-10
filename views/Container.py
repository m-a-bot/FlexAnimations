from typing import Optional
from settings import ROOT_DIR
from sections.volume_slider import VolumeSliderSection
from arcade.experimental.uislider import UISlider
import arcade
import arcade.gui
import arcade.gui.events
from arcade.gui.widgets import _Rect
import os
from tkinter.filedialog import askopenfilename
from settings import ROOT_DIR


SIZE_BUTTON = 40
SPACE_BETWEEN_BUTTONS = 60

class ContainerView(arcade.View):

    def __init__(self):

        super().__init__()

        self.sound_off = True
        self.paused = False
        self.cur_song_index = 0
        self.songs = [":resources:music/1918.mp3"]
        self.hud_is_visible = False
        # self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
        

        self.setup()
        
        # self.ui_manager.add(layout)
        
        # self.section = VolumeSliderSection(layout.right - SPACE_BETWEEN_BUTTONS - SIZE_BUTTON / 2 + 6.5, self.btn_sound_on.top + 60, 10, 100)
        # self.section.enabled=False
        # self.section_manager.add_section(self.section)


    def setup(self):
        
        # UIManager
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.main_layout = arcade.gui.UILayout(0, 0, self.window.width, self.window.height)

        self.ui_manager.add(self.main_layout.with_background(arcade.make_soft_square_texture(100, arcade.color_from_hex_string("#346734"), outer_alpha=255)))

        self.player_bar = arcade.gui.UILayout(0, 0, self.window.width, 80)
        self.buttons = arcade.gui.UIBoxLayout(vertical=False)
        self.center_buttons = arcade.gui.UIBoxLayout(vertical=False)

        # gear
        self.btn_gear = self.add_texture_button(
            os.path.join(ROOT_DIR, "resources/icons/icons8-горизонтальный-микшер-настроек-96.png"),
            0.5
        )
        self.btn_gear.on_click = self.btn_gear_clicked
        self.buttons.add(self.btn_gear)


        # star_square
        self.btn_star_square = self.add_texture_button(
            os.path.join(ROOT_DIR, "resources/icons/icons8-история-деятельности-96.png"),0.5
        )
        # add event
        # self.btn_play.on_click = 
        self.center_buttons.add(self.btn_star_square)

        # play
        self.btn_play = self.add_texture_button(
            os.path.join(ROOT_DIR, "resources/icons/icons8-play-в-круге-96.png"),0.5
        )
        # add event
        self.btn_play.on_click = self.btn_play_clicked
        self.center_buttons.add(self.btn_play)

        # up
        self.btn_up = self.add_texture_button(
            os.path.join(ROOT_DIR, "resources/icons/icons8-добавить-файл-96.png"),0.5
        )
        # add event
        self.btn_up.on_click = self.upload
        self.center_buttons.add(self.btn_up)

        self.buttons.add(self.center_buttons)

        # sound_on
        self.btn_sound_on = self.add_texture_button(
            os.path.join(ROOT_DIR, "resources/icons/icons8-громкий-звук-96.png"),0.5
        )
        self.btn_sound_on.on_click = self.btn_sound_clicked
        self.buttons.add(self.btn_sound_on)

        self.player_bar.add(arcade.gui.UIAnchorWidget(child=self.buttons, anchor_y="bottom", align_y=20, size_hint=(1,0)))

        self.main_layout.add(self.player_bar.with_background(
            arcade.make_soft_square_texture(100, (150,150,150,255), outer_alpha=255)))
        
        self.slider = UISlider(value=50, width=150, y=85).with_background(arcade.make_soft_square_texture(50, arcade.color_from_hex_string("#E3E3E3"), outer_alpha=255), 5, 2, 5, 2)

        self.slider = arcade.gui.UIAnchorWidget(child=self.slider, anchor_x="right", align_x=-5, anchor_y="bottom", align_y=85)

        self.ui_manager.add(self.main_layout)

    def on_resize(self, width: int, height: int):
        
        super().on_resize(width, height)

        self.main_layout._rect = _Rect(0,0,width, height)
        self.player_bar._rect = _Rect(0,0,width, 80)

        if width <= 500:
            self.buttons._space_between = width // 10
            self.center_buttons._space_between = 10
        elif width <= 768:
            self.buttons._space_between = width // 5.7
            self.center_buttons._space_between = 20
        elif width <= 1024:
            self.buttons._space_between = width // 4.4
            self.center_buttons._space_between = 70
        elif width <= 1366:
            self.buttons._space_between = width // 4
            self.center_buttons._space_between = 75
        else:
            self.buttons._space_between = width // 3
            self.center_buttons._space_between = 80


    def add_texture_button(self, texture_name, scale=1):

        __texture = arcade.load_texture(texture_name) 

        return arcade.gui.UITextureButton(
            texture = __texture,
            scale = scale
        )


    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#BABAB4"))


    def on_draw(self):
        self.clear()
        arcade.start_render()

        
        # arcade.draw_xywh_rectangle_filled(self.window.width//6, 0, self.window.width//1.5, 80, arcade.color_from_hex_string("#E1DFDF"))
        self.ui_manager.draw()
        arcade.draw_text(self.window.width, 20, self.window.height - 50)
    
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
            
            self.ui_manager.add(self.slider)

            self.sound_off = False
        else:
            self.ui_manager.remove(self.slider)

            self.sound_off = True


    def set_pause(self):
        self.btn_play.texture = arcade.load_texture(os.path.join(ROOT_DIR, "resources/icons/icons8-пауза-в-кружке-96.png"))

        
    def set_play(self):
        self.btn_play.texture = arcade.load_texture(os.path.join(ROOT_DIR, "resources/icons/icons8-play-в-круге-96.png"))
        

    def upload(self, *_):
        filename = askopenfilename()
        self.songs.append(filename)
        print(self.songs)


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
    
    