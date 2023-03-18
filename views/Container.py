import arcade
import numpy
import numpy.random
from assets.MovementSprite import MovementSprite
from typing import Optional
from settings import ROOT_DIR, resource_path
from arcade.experimental.uislider import UISlider
import arcade
import arcade.gui
import arcade.gui.events
from arcade.gui.widgets import _Rect
import os
from tkinter.filedialog import askopenfilename
from settings import ROOT_DIR
from scipy.io import wavfile


SIZE_BUTTON = 40
SPACE_BETWEEN_BUTTONS = 60

class ContainerView(arcade.View):

    def __init__(self):

        super().__init__()
        
        self.setup()
        self.load_textures()
        self.add_figures()
        
        self.bg = arcade.load_texture(":resources:images/backgrounds/stars.png")
        

    def add_figures(self):
        self.figures = arcade.SpriteList()

        x = [-3, -1, 1, 3]
        y = [-3, -2, 2, 3]

        scales = [0.6, 1, 1.1, 0.7, 1.3, 0.9]

        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:onscreen_controls/shaded_light/wrench.png",
                                           center_x=200,
                                           center_y=100,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:onscreen_controls/shaded_light/select.png",
                                           center_x=100,
                                           center_y=200,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/cards/cardSpadesJ.png",
                                           center_x=150,
                                           center_y=150,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/cards/cardHearts3.png",
                                           center_x=300,
                                           center_y=300,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y),
                                           texture=arcade.make_circle_texture(60, arcade.color_from_hex_string("#123fdc")),
                                           center_x=330,
                                           center_y=250,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y),
                                           texture=arcade.make_soft_square_texture(90, arcade.color_from_hex_string("#123fdc")),
                                           center_x=250,
                                           center_y=120,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/space_shooter/meteorGrey_big1.png",
                                           center_x=300,
                                           center_y=300,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/test_textures/xy_square.png",
                                           center_x=500,
                                           center_y=100,
                                           scale=numpy.random.choice(scales)))


    def load_textures(self):

        try:
            self.play_texture = arcade.load_texture(resource_path(os.path.join(ROOT_DIR, "resources/icons/icons8-play-в-круге-96.png")))
            self.stop_texture = arcade.load_texture(resource_path(os.path.join(ROOT_DIR, "resources/icons/icons8-пауза-в-кружке-96.png")))
        except:
            ...


    def setup(self):
        
        # UIManager
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.main_layout = arcade.gui.UILayout(0, 0, self.window.width, self.window.height)

        self.ui_manager.add(self.main_layout)

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

        self.player_bar_bg = self.player_bar.with_background(arcade.make_soft_square_texture(100, (150,150,150,255), outer_alpha=255))
        # self.player_bar.on_event = self.update_visibility_player_bar

        self.main_layout.add(self.player_bar_bg)
        
        self.slider = UISlider(value=50, width=150, y=85).with_background(arcade.make_soft_square_texture(50, arcade.color_from_hex_string("#E3E3E3"), outer_alpha=255), 5, 2, 5, 2)

        self.slider = arcade.gui.UIAnchorWidget(child=self.slider, anchor_x="right", align_x=-5, anchor_y="bottom", align_y=85)

        self.ui_manager.add(self.main_layout)

    def on_resize(self, width: int, height: int):
        
        super().on_resize(width, height)

        # MovementSprite.width = self.window.width
        # MovementSprite.height = self.window.height

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

    def on_update(self, delta_time: float):
    # count_figures = len(self.figures)
    # for i in range(count_figures-1):
    #     for j in range(1, count_figures):
    #         if arcade.check_for_collision(self.figures[i], self.figures[j]):
    #             self.figures[i].strafe()

        self.figures.update()


    def update_visibility_player_bar(self, event):
        
        if isinstance(event, arcade.gui.events.UIMouseMovementEvent):
            
            if self.player_bar._rect.collide_with_point(event.x, event.y):
                self.hud_is_visible = True

            else:
                self.hud_is_visible = False
            

    def add_texture_button(self, texture_name, scale=1):
        
        try:
            __texture = arcade.load_texture(resource_path(texture_name)) 
        
            return arcade.gui.UITextureButton(
                texture = __texture,
                scale = scale
            )
        except Exception as error:
            print(error)

    def on_draw(self):
        self.clear()
        arcade.start_render()
        
        arcade.draw_lrwh_rectangle_textured(0,0, self.window.width, self.window.height, self.bg)

        self.figures.draw()
        self.ui_manager.draw()

        # arcade.draw_xywh_rectangle_filled(self.window.width//6, 0, self.window.width//1.5, 80, arcade.color_from_hex_string("#E1DFDF"))
        
        arcade.draw_text(self.window.width, 20, self.window.height - 50)
    

    def on_mouse_motion(self, x, y, dx, dy):
        if self.player_bar._rect.collide_with_point(x,y):
            self.hud_is_visible = True
        else:
            self.hud_is_visible = False 

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
        self.btn_play.texture = self.stop_texture

    def set_play(self):
        self.btn_play.texture = self.play_texture
        

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
        
        arcade.draw_lrwh_rectangle_textured(0,0,self.window.width, self.window.height, self.bg)
        self.figures.draw()

        self.ui_manager.draw()


    def btn_close_clicked(self, *_):
        view = ContainerView()
        self.window.show_view(view)
    
