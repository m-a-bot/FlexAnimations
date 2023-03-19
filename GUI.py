import arcade
import arcade.gui
from sections.music_track import MusicTrack
from sections.menu import Menu
from tkinter.filedialog import askopenfilename
from arcade.experimental.uislider import UISlider
from scipy.io import wavfile
from arcade.experimental import Shadertoy


SCALE_BUTTONS = 0.7

class GUI(arcade.View):

    def __init__(self):
        super().__init__()
        # region
        self.set_location = (0, 0)
        self.width = self.window.width
        self.height = self.window.height
        self.hud_height = self.height // 8
        # endregion

        self.bg = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

        self.time = 0.0
        # shader_source = None
        # shader_file_path = "scripts/shaders/Image.glsl"

        # with open(shader_file_path) as file:

        #     shader_source = file.read()
        
        # self.shadertoy = Shadertoy(self.window.get_size(), main_source=shader_source)
        
        self.paused = True  # True, если музыка играет, False, если пауза
        self.hud_is_visible = False  # виден ли плеер
        self.sound_bar_is_visible = False  # видна ли планка с саундом
        self.volume_level = 50  # уровень громкости
        self.songs = ["resources/music/Rammstein_-_AUSLNDER_64649307.wav","resources/music/follow.wav","resources/music/Rammstein_-_Deutschland_63121881.wav",
                      "resources/music/Rammstein_-_Keine_Lust_63121988.wav","resources/music/Rammstein_-_Ohne_Dich_63121957.wav"
                        ]
        self.cur_song_index = 0
        self.media_player = None
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])

        samplerate, self.mdata = wavfile.read(self.songs[self.cur_song_index])

        self.music_track = MusicTrack(25, self.hud_height + 50, self.width - 50, 100)
        self.music_track.enabled = False
        self.music_track.music_data = self.mdata[:,0]

        self.menu = Menu(self.width//8, self.height//10 - 50, self.width//4*3, self.height//10 * 8)

        self.section_manager.add_section(self.music_track)
        self.section_manager.add_section(self.menu)

        self.setup_gui()

        self.slider = UISlider(value=self.volume_level, x=self.volume.left, y=self.hud_height + 5, width=180, height=40)
        self.slider.on_change = self.set_player_volume

        
    def update(self, delta_time: float):
        super().on_update(delta_time)

        self.time += delta_time



    def setup_gui(self):

        self.ui_manager = arcade.gui.UIManager()

        self.height_player_bar = 80

        self.player_bar = arcade.gui.UILayout(0, 0, self.window.width, self.height_player_bar)
        self.buttons = arcade.gui.UIBoxLayout(vertical=False, space_between=self.width // 3.5)
        self.center_buttons = arcade.gui.UIBoxLayout(vertical=False, space_between=85)

        # Settings button
        self.settings = self.add_texture_button(
            texture_file_name=":resources:onscreen_controls/flat_dark/gear.png",
            hover_texture_file_name=":resources:onscreen_controls/shaded_dark/gear.png",
            press_texture_file_name=":resources:onscreen_controls/shaded_dark/gear.png",
            _scale=1.5 * SCALE_BUTTONS
        )

        self.settings.on_click = self.open_settings  # type: ignore                                        
        self.buttons.add(self.settings)

        # Star button
        self.star = self.add_texture_button(
            texture_file_name=":resources:onscreen_controls/flat_dark/star_square.png",
            hover_texture_file_name=":resources:onscreen_controls/shaded_dark/star_square.png",
            press_texture_file_name=":resources:onscreen_controls/shaded_dark/star_square.png",
            _scale=1.5 * SCALE_BUTTONS
        )

        self.center_buttons.add(self.star)

        # Play/pause button

        self.play_button = self.add_texture_button(
            texture_file_name=":resources:onscreen_controls/flat_dark/play.png",
            hover_texture_file_name=":resources:onscreen_controls/shaded_dark/play.png",
            press_texture_file_name=":resources:onscreen_controls/shaded_dark/play.png",
            _scale=1.5 * SCALE_BUTTONS
        )

        self.play_button.on_click = self.play_button_clicked  # type: ignore                               
        self.center_buttons.add(self.play_button)

        # Up button
        self.up = self.add_texture_button(
            texture_file_name=":resources:onscreen_controls/flat_dark/up.png",
            hover_texture_file_name=":resources:onscreen_controls/shaded_dark/up.png",
            press_texture_file_name=":resources:onscreen_controls/shaded_dark/up.png",
            _scale=0.9 * SCALE_BUTTONS
        )

        self.up.on_click = self.upload
        self.center_buttons.add(self.up)

        # Volume button
        self.volume = self.add_texture_button(
            texture_file_name=":resources:onscreen_controls/flat_dark/sound_on.png",
            hover_texture_file_name=":resources:onscreen_controls/shaded_dark/sound_on.png",
            press_texture_file_name=":resources:onscreen_controls/shaded_dark/sound_on.png",
            _scale=1.5 * SCALE_BUTTONS
        )

        self.volume.on_click = self.switch_sound_bar  # type: ignore

        self.buttons.add(self.center_buttons)
        self.buttons.add(self.volume)

        self.player_bar.add(arcade.gui.UIAnchorWidget(child=self.buttons, anchor_y="bottom", align_y=20))

        self.up_down = self.add_texture_button(
            texture_file_name=":resources:onscreen_controls/flat_dark/up.png",
            hover_texture_file_name=":resources:onscreen_controls/shaded_dark/up.png",
            press_texture_file_name=":resources:onscreen_controls/shaded_dark/up.png",
            _scale=0.9 * SCALE_BUTTONS * 0.5
        )

        self.up_down.on_click = self.up_down_button_clicked  # type: ignore     

        self.ui_manager.add(self.player_bar)

        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=self.up_down, anchor_y="bottom", align_y=self.hud_height + 15))

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

        self.hud_is_visible = False

    def play_button_on(self):
        self.play_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/pause_square.png")
        self.play_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/pause_square.png")
        self.play_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/pause_square.png")

    def play_button_off(self):
        self.play_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/play.png")
        self.play_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        self.play_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/play.png")

        # сам медиа-плеер

    def music_over(self):
        self.media_player.pop_handlers()
        self.media_player = None
        self.play_button_off()
        self.cur_song_index += 1
        self.music_track.current_song_index=0

        if self.cur_song_index >= len(self.songs):
            self.cur_song_index = 0
            
            self.paused = True
            self.play_button_off()
            self.music_track.enabled=False
        if not self.paused:
            self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
            self.media_player = self.my_music.play(volume=self.volume_level / 100)
            self.media_player.push_handlers(on_eos=self.music_over)

            samplerate, self.mdata = wavfile.read(self.songs[self.cur_song_index])
            self.music_track.music_data = self.mdata[:,0]

    def play_button_clicked(self, *_):
        self.paused = False
        self.music_track.enabled = True
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

        # HUD

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.bg)
        # mouse_pos = self.window.mouse["x"], self.window.mouse["y"]
        # self.shadertoy.render(time=self.time, mouse_position=mouse_pos)
        
        if self.hud_is_visible or self.sound_bar_is_visible:
            arcade.draw_xywh_rectangle_filled(0, 0, self.width, self.hud_height, (0,0,0, 90))
            
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

    #TODO
    #доделать
    def up_down_button_clicked(self, *_):
        
        self.music_track.enabled = not self.music_track.enabled

    # загрузка песен

    def upload(self, *_):
        filename = askopenfilename()
        self.songs.append(filename)

        # показывает/убирает hud в зависимости от положения мыши

    def on_mouse_motion(self, x, y, dx, dy):
        if y < self.hud_height + 50:

            self.hud_is_visible = True
            self.music_track._bottom = self.hud_height + 50
        else:
            self.hud_is_visible = False
            self.music_track._bottom = 25

    #TODO
    """
    Исправить баг
    плеер не скрывается, когда активен slider
    """
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

        


    def show_sound_bar(self, *_):
        arcade.draw_lrtb_rectangle_filled(self.width * .968 - self.width // 100, self.width * .968 + self.width // 100,
                                          self.height // 4, self.height // 8 + self.height // 225, arcade.color.GRAY)
        arcade.draw_line(self.width * .968, self.height // 7, self.width * .968, self.height // 4 - self.height // 65,
                         arcade.color.WHITE, line_width=5)
        arcade.draw_line(self.width * .968 - self.width // 150, self.height // 7 + self.volume_level,
                         self.width * .968 + self.width // 150, self.height // 7 + self.volume_level,
                         arcade.color.WHITE, line_width=5)

    # mouse-press ивенты
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:

            if not self.slider._rect.collide_with_point(x,y):
                self.sound_bar_is_visible = False
                self.ui_manager.remove(self.slider)

    def set_player_volume(self, *_):

        if self.media_player:
            self.media_player.volume = self.slider.value / 100
