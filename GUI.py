from math import degrees
import random
import arcade
import arcade.gui
from sections.music_track import MusicTrack
from sections.menu import Menu
from sections._settings import SettingsView
from tkinter.filedialog import askopenfilename
from arcade.experimental.uislider import UISlider
from scipy.io import wavfile
import pymunk
from assets.scripts.Render import *
from assets.MovementSprite import PhysicsSprite
import os

PINK = (238, 20, 223)
SCALE_BUTTONS = 0.7
DEBUG = True


class GUI(arcade.View):
    def __init__(self):
        super().__init__()
        self.set_location = (0, 0)
        self.width = self.window.width
        self.height = self.window.height
        self.hud_height = self.height // 8
        self.bg = arcade.load_texture("resources/icons/фон.png")
        self.text = arcade.Text("", 50, self.height - 50, PINK, 14)

        self.time = 0.0

        try:
            os.remove('resources/icons/current_figure.png')
        except:
            pass

        self.play_animations = False

        self.paused = True
        self.hud_is_visible = False
        self.sound_bar_is_visible = False
        self.volume_level = 50

        self.songs = ["resources/music/Rammstein_-_Keine_Lust_63121988.wav",
                      "resources/music/follow.wav", "resources/music/Rammstein_-_Deutschland_63121881.wav"]

        self.cur_song_index = 0
        self.media_player = None
        self.my_music = self.load_wav()
        samplerate, self.mdata = self.get_music_data()
        self.music_track = MusicTrack(25, self.hud_height + 50, self.width - 50, 100)
        self.music_track.enabled = False
        if self.mdata is not None:
            self.music_track.set_music_data(samplerate, self.mdata[:, 0])

        self.menu = Menu(self, self.music_track)
        self.menu.animation = None
        self.menu.pre_animation = self.menu.animation

        self.section_manager.add_section(self.music_track)

        self.setup_gui()
        self.slider = UISlider(value=self.volume_level, x=self.volume.left, y=self.hud_height + 5, width=120, height=40,
                               style={"normal_filled_bar": (238, 20, 223), "hovered_filled_bar": (238, 20, 223),
                                      "pressed_filled_bar": (238, 20, 223)})
        self.slider.on_change = self.set_player_volume

    def rebase_gui_sprites_texture(self, texture):
        if len(self.menu.gui_sprites) == 0:
            try:
                os.remove('resources/icons/current_figure.png')
            except:
                pass
            img = texture.image.resize((60, 60))

            img.save('resources/icons/current_figure.png')
        else:
            for sprite in self.menu.gui_sprites:
                sprite.texture = texture
                sprite.scale = 0.5

    def update(self, delta_time: float):

        self.time += delta_time

        if self.menu.gui_animation is not None and self.play_animations:
            self.menu.gui_animation.animation_run(self.menu.gui_sprites, delta_time)

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.bg)
        self.menu.gui_sprites.draw()

        if DEBUG:
            if len(self.songs) > 0:
                self.text.text = f"{self.cur_song_index + 1}/{len(self.songs)} - {self.songs[self.cur_song_index]}"
                self.text.draw()

        if self.hud_is_visible or self.sound_bar_is_visible:
            arcade.draw_xywh_rectangle_filled(0, 0, self.width, self.hud_height, (0, 0, 0, 90))
            arcade.draw_line(0, self.hud_height, self.width, self.hud_height, arcade.color.BLACK, line_width=5)
            self.ui_manager.enable()
            self.ui_manager.draw()

            if self.media_player:
                arcade.draw_circle_filled(
                    (self.media_player.time / arcade.Sound.get_length(self.media_player)) * self.width,
                    self.hud_height, self.width // 150, arcade.color.RED)
                arcade.draw_line(0, self.hud_height,
                                 (self.media_player.time / arcade.Sound.get_length(self.media_player)) * self.width,
                                 self.hud_height, arcade.color.RED, line_width=5)

        else:
            self.ui_manager.disable()

    def setup_gui(self):

        self.ui_manager = arcade.gui.UIManager()

        self.height_player_bar = 80

        self.player_bar = arcade.gui.UILayout(0, 0, self.window.width, self.height_player_bar)
        self.buttons = arcade.gui.UIBoxLayout(vertical=False, space_between=self.width // 4.8)
        self.center_buttons = arcade.gui.UIBoxLayout(vertical=False, space_between=65)

        self.settings = self.add_texture_button(
            texture_file_name="resources/icons/icons8-настройки-96.png",
            hover_texture_file_name="resources/icons/icons8-настройки-96.png",
            press_texture_file_name="resources/icons/icons8-настройки-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.settings.on_click = self.open_settings1
        self.buttons.add(self.settings)

        self.star = self.add_texture_button(
            texture_file_name="resources/icons/icons8-звездочка-96.png",
            hover_texture_file_name="resources/icons/icons8-звездочка-96.png",
            press_texture_file_name="resources/icons/icons8-звездочка-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )
        self.star.on_click = self.open_settings
        self.center_buttons.add(self.star)

        self.left_button = self.add_texture_button(
            texture_file_name="resources/icons/icons8-предыдущий трек-96.png",
            hover_texture_file_name="resources/icons/icons8-предыдущий трек-96.png",
            press_texture_file_name="resources/icons/icons8-предыдущий трек-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.left_button.on_click = self.left_button_clicked
        self.center_buttons.add(self.left_button)

        self.play_button = self.add_texture_button(
            texture_file_name="resources/icons/icons8-play-в-круге-96.png",
            hover_texture_file_name="resources/icons/icons8-play-в-круге-96.png",
            press_texture_file_name="resources/icons/icons8-play-в-круге-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.play_button.on_click = self.play_button_clicked
        self.center_buttons.add(self.play_button)

        self.right_button = self.add_texture_button(
            texture_file_name="resources/icons/icons8-следующий трек-96.png",
            hover_texture_file_name="resources/icons/icons8-следующий трек-96.png",
            press_texture_file_name="resources/icons/icons8-следующий трек-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.right_button.on_click = self.right_button_clicked
        self.center_buttons.add(self.right_button)

        self.up = self.add_texture_button(
            texture_file_name="resources/icons/icons8-добавить-файл-96.png",
            hover_texture_file_name="resources/icons/icons8-добавить-файл-96.png",
            press_texture_file_name="resources/icons/icons8-добавить-файл-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.up.on_click = self.upload
        self.center_buttons.add(self.up)

        self.volume = self.add_texture_button(
            texture_file_name="resources/icons/icons8-громкий-звук-96.png",
            hover_texture_file_name="resources/icons/icons8-громкий-звук-96.png",
            press_texture_file_name="resources/icons/icons8-громкий-звук-96.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.volume.on_click = self.switch_sound_bar

        self.buttons.add(self.center_buttons)
        self.buttons.add(self.volume)

        self.player_bar.add(arcade.gui.UIAnchorWidget(child=self.buttons, anchor_y="bottom", align_y=20))

        self.up_down = self.add_texture_button(
            texture_file_name="resources/icons/icons8-скрыть-показать-дорожку-96.png",
            hover_texture_file_name="resources/icons/icons8-скрыть-показать-дорожку-96.png",
            press_texture_file_name="resources/icons/icons8-скрыть-показать-дорожку-96.png",
            _scale=0.6 * SCALE_BUTTONS
        )
        self.up_down.on_click = self.up_down_button_clicked
        self.ui_manager.add(self.player_bar)
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(child=self.up_down, anchor_y="bottom", align_y=self.hud_height + 15))

    def add_ph_sprite(self, texture, position, direction, mass, elasticity, body_type, pfile=None, scale=1):

        if pfile is None:
            self.sprites.append(
                PhysicsSprite(self.sim.Space, position, mass, body_type, elasticity, direction, _texture=texture,
                              sprite_scale=scale))
        else:
            self.sprites.append(
                PhysicsSprite(self.sim.Space, position, mass, body_type, elasticity, direction, file_name=pfile,
                              sprite_scale=scale))

    def setup_simulation(self):
        mass = 10
        elasticity = 0.9
        dynamic = pymunk.Body.DYNAMIC

        color = (255, 0, 0)
        size = 50
        texture = arcade.make_circle_texture(size, color)
        for _ in range(3):
            position = (random.randint(size, self.width - 50), random.randint(50, self.height - 50))
            direction = (random.choice([-10, 10]), random.choice([-10, 10]))

            self.add_ph_sprite(texture, position, direction, mass, elasticity, dynamic)

        mass = 1
        texture = arcade.make_soft_square_texture(40, (0, 0, 255), outer_alpha=255)
        for _ in range(2):
            position = (random.randint(50, self.width - 50), random.randint(50, self.height - 50))
            direction = (random.choice([-10, 10]), random.choice([-10, 10]))

            self.add_ph_sprite(texture, position, direction, mass, elasticity, dynamic, scale=0.9)

        r_grad = arcade.Texture("rect_grad", image=get_rectangle_gradient(120, 120, (120, 120, 9), (255, 45, 129)))
        triangle1 = arcade.Texture("triangle1", image=get_triangle_random(90, 100))

        for _ in range(4):
            position = (random.randint(50, self.width - 50), random.randint(50, self.height - 50))
            direction = (random.choice([-10, 10]), random.choice([-10, 10]))

            self.add_ph_sprite(r_grad, position, direction, mass, elasticity, dynamic, scale=1)

        for _ in range(2):
            position = (random.randint(50, self.width - 50), random.randint(50, self.height - 50))
            direction = (random.choice([-10, 10]), random.choice([-10, 10]))

            self.add_ph_sprite(triangle1, position, direction, mass, elasticity, dynamic, scale=1)

        self.sim.set_sprites(self.sprites)

    def add_texture_button(self,
                           texture_file_name: str,
                           hover_texture_file_name: str,
                           press_texture_file_name: str,
                           _scale: float = 1,
                           _x: float = 0,
                           _y: float = 0):

        normal_texture = arcade.load_texture(texture_file_name)

        hover_texture = arcade.load_texture(hover_texture_file_name)

        press_texture = arcade.load_texture(press_texture_file_name)

        return arcade.gui.UITextureButton(
            x=_x,
            y=_y,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale=_scale
        )

    def open_settings(self, *_):
        self.menu.enabled = True
        self.menu.previous_animation = self.menu.animation
        self.window.show_view(self.menu)
        self.hud_is_visible = False

    def open_settings1(self, *_):
        self.menu.pre_figure = None
        self.window.show_view(SettingsView(self))

    def play_button_on(self):
        self.play_button.texture_pressed = \
            arcade.load_texture("resources/icons/icons8-pause-в-круге-96.png")
        self.play_button.texture = \
            arcade.load_texture("resources/icons/icons8-pause-в-круге-96.png")
        self.play_button.texture_hovered = \
            arcade.load_texture("resources/icons/icons8-pause-в-круге-96.png")

    def play_button_off(self):
        self.play_button.texture_pressed = \
            arcade.load_texture("resources/icons/icons8-play-в-круге-96.png")
        self.play_button.texture = \
            arcade.load_texture("resources/icons/icons8-play-в-круге-96.png")
        self.play_button.texture_hovered = \
            arcade.load_texture("resources/icons/icons8-play-в-круге-96.png")

    def music_over(self):
        self.media_player.pop_handlers()
        self.media_player = None
        self.play_button_off()
        self.cur_song_index += 1
        self.music_track.current_song_index = 0
        self.play_animations = False

        if self.cur_song_index >= len(self.songs):
            self.cur_song_index = 0
            self.play_animations = True
            self.paused = True
            self.play_button_off()
            self.music_track.enabled = False
        elif not self.paused:
            self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_animations = True
            samplerate, self.mdata = self.get_music_data()

            print(samplerate)
            self.music_track.set_music_data(samplerate, self.mdata[:, 0])

    def load_wav(self):
        if len(self.songs) == 0:
            return
        return arcade.load_sound(self.songs[self.cur_song_index])

    def get_music_data(self):
        if len(self.songs) == 0:
            return None, None
        return wavfile.read(self.songs[self.cur_song_index])

    def left_button_clicked(self, *_):
        self.cur_song_index = max(0, self.cur_song_index - 1)
        samplerate, self.mdata = self.get_music_data()

        if self.mdata is None:
            return
        self.music_track.set_music_data(samplerate, self.mdata[:, 0])
        self.my_music = self.load_wav()

        if self.media_player is not None:
            self.media_player.pause()
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_button_on()
        else:
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_button_on()

    def right_button_clicked(self, *_):
        self.cur_song_index = min(self.cur_song_index + 1, len(self.songs) - 1)
        self.my_music = self.load_wav()
        samplerate, self.mdata = self.get_music_data()

        if self.mdata is None:
            return
        self.music_track.set_music_data(samplerate, self.mdata[:, 0])

        if self.media_player is not None:
            self.media_player.pause()
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_button_on()
        else:
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_button_on()

    def play_button_clicked(self, *_):
        self.paused = False
        self.music_track.enabled = True
        if self.my_music is None:
            return

        self.play_animations = not self.play_animations
        if not self.media_player:
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_button_on()
        elif not self.media_player.playing:
            self.media_player.play()
            self.media_player.volume = self.volume_level / 100
            self.play_button_on()
        elif self.media_player.playing:
            self.music_track.enabled = False
            self.media_player.pause()
            self.play_button_off()

    def up_down_button_clicked(self, *_):
        self.music_track.enabled = not self.music_track.enabled

    def upload(self, *_):
        filename = askopenfilename()
        if filename == "":
            return
        self.songs.append(filename)

        if len(self.songs) == 1:

            self.my_music = self.load_wav()
            samplerate, self.mdata = self.get_music_data()

            if self.mdata is None:
                return
            self.music_track.set_music_data(samplerate, self.mdata[:, 0])

    def on_mouse_motion(self, x, y, dx, dy):
        if y < self.hud_height + 50:

            self.hud_is_visible = True
            self.music_track._bottom = self.hud_height + 50
        else:

            self.hud_is_visible = False
            self.music_track._bottom = 25
            self.sound_bar_is_visible = False
            self.ui_manager.remove(self.slider)

    def switch_sound_bar(self, *_):
        self.sound_bar_is_visible = not self.sound_bar_is_visible

        if self.sound_bar_is_visible:
            self.ui_manager.add(self.slider)
        else:
            self.ui_manager.remove(self.slider)

    def on_update(self, delta_time):

        if self.media_player is not None:

            if self.media_player.playing:
                self.music_track.current_song_index += 1

        self.music_track.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:

            if not self.slider._rect.collide_with_point(x, y):
                self.sound_bar_is_visible = False
                self.ui_manager.remove(self.slider)

    def set_player_volume(self, *_):

        if self.media_player:
            self.media_player.volume = self.slider.value / 100
