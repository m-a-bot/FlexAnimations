import arcade
import arcade.gui
from sections.volume_slider import VolumeSliderSection
from tkinter.filedialog import askopenfilename


class GUI(arcade.View):


    def __init__(self, fullscreen = False):
        super().__init__(fullscreen)
        #region
        self.set_location = (0, 0)
        self.width = self.window.width
        self.height = self.window.height
        #endregion
        arcade.set_background_color(arcade.color.WENGE) #ставим бэк
        self.paused = True #True, если музыка играет, False, если пауза
        self.hud_is_visible = False #виден ли плеер
        self.sound_bar_is_visible = False #видна ли планка с саундом 
        self.volume_level = 50 #уровень громкости 
        self.songs = [":resources:music/1918.mp3"] 
        self.cur_song_index = 0 
        self.media_player = None
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
        
        self.setup_gui()

        # self.volume_slider = VolumeSliderSection(self.volume.center_x)

    def setup_gui(self):

        self.ui_manager = arcade.gui.UIManager()

        self.height_player_bar = 80

        self.player_bar = arcade.gui.UILayout(0, 0, self.window.width, self.height_player_bar)
        self.buttons = arcade.gui.UIBoxLayout(vertical=False, space_between=self.width//4)
        self.center_buttons = arcade.gui.UIBoxLayout(vertical=False, space_between=75)


        # Settings button
        self.settings = self.add_texture_button(
            texture_file_name = ":resources:onscreen_controls/flat_dark/gear.png",
            hover_texture_file_name = ":resources:onscreen_controls/shaded_dark/gear.png",
            press_texture_file_name = ":resources:onscreen_controls/shaded_dark/gear.png",
            _scale = 1.5
        )
        
        self.settings.on_click = self.open_settings  # type: ignore                                        
        self.buttons.add(self.settings)


        # Star button
        self.star = self.add_texture_button(
            texture_file_name = ":resources:onscreen_controls/flat_dark/star_square.png",
            hover_texture_file_name = ":resources:onscreen_controls/shaded_dark/star_square.png",
            press_texture_file_name = ":resources:onscreen_controls/shaded_dark/star_square.png",
            _scale = 1.5
        )
        
        self.center_buttons.add(self.star)

        # Play/pause button

        self.play_button = self.add_texture_button(
            texture_file_name = ":resources:onscreen_controls/flat_dark/play.png",
            hover_texture_file_name = ":resources:onscreen_controls/shaded_dark/play.png",
            press_texture_file_name = ":resources:onscreen_controls/shaded_dark/play.png",
            _scale = 1.5
        )

        self.play_button.on_click = self.play_button_clicked  # type: ignore                               
        self.center_buttons.add(self.play_button)
        

        # Up button
        self.up = self.add_texture_button(
            texture_file_name = ":resources:onscreen_controls/flat_dark/up.png",
            hover_texture_file_name = ":resources:onscreen_controls/shaded_dark/up.png",
            press_texture_file_name = ":resources:onscreen_controls/shaded_dark/up.png",
            _scale = 0.9
        )
        
        self.up.on_click = self.upload
        self.center_buttons.add(self.up)
        
        
        # Volume button
        self.volume = self.add_texture_button(
            texture_file_name = ":resources:onscreen_controls/flat_dark/sound_on.png",
            hover_texture_file_name = ":resources:onscreen_controls/shaded_dark/sound_on.png",
            press_texture_file_name = ":resources:onscreen_controls/shaded_dark/sound_on.png",
            _scale = 1.5
        )
        
        self.volume.on_click = self.switch_sound_bar  # type: ignore

        self.buttons.add(self.center_buttons)
        self.buttons.add(self.volume)                                                

        self.player_bar.add(arcade.gui.UIAnchorWidget(child=self.buttons, anchor_y="bottom", align_y=20))

        self.ui_manager.add(self.player_bar)

    def add_texture_button(self, 
        texture_file_name : str,
        hover_texture_file_name : str,
        press_texture_file_name : str,
        _scale : float = 1,
        _x : float = 0,
        _y : float = 0):

        
        normal_texture = arcade.load_texture(texture_file_name)

        hover_texture = arcade.load_texture(hover_texture_file_name)

        press_texture = arcade.load_texture(press_texture_file_name)

        
        return arcade.gui.UITextureButton(
            x = _x,
            y = _y,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale = _scale
        )

    def open_settings(self, *_):
        # сюда дописывать код для кнопки настроек
        ...
        
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
        if self.cur_song_index >= len(self.songs):
            self.cur_song_index = 0
            self.paused = True
            self.play_button_off()
        if not self.paused:
            self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
            self.media_player = self.my_music.play(volume = self.volume_level/100)
            self.media_player.push_handlers(on_eos=self.music_over)
        
    def play_button_clicked(self, *_):
        self.paused = False
        if not self.media_player:
            self.media_player = self.my_music.play(volume = self.volume_level/100)
            self.media_player.push_handlers(on_eos=self.music_over)
            self.play_button_on()
        elif not self.media_player.playing:
            self.media_player.play()
            self.media_player.volume = self.volume_level/100  
            self.play_button_on()
        elif self.media_player.playing:
            self.media_player.pause()
            self.play_button_off()
        
        #HUD 
    def on_draw(self):
        self.clear()
        if self.hud_is_visible or self.sound_bar_is_visible:
            arcade.draw_line(0, self.height//12, self.width, self.height//12, arcade.color.ALMOND, line_width = self.height//6)
            arcade.draw_line(0, self.height//6, self.width, self.height//6, arcade.color.BLACK, line_width = 5)
            self.ui_manager.enable()
            self.ui_manager.draw()
            if self.sound_bar_is_visible:
                self.show_sound_bar()
            if self.media_player:
                arcade.draw_circle_filled((self.media_player.time/arcade.Sound.get_length(self.media_player))*self.width, self.height//6, self.width//150, arcade.color.RED)
                arcade.draw_line(0, self.height//6, (self.media_player.time/arcade.Sound.get_length(self.media_player))*self.width, self.height//6, arcade.color.RED, line_width = 5)
        else:
            self.ui_manager.disable()

        # загрузка песен
    def upload(self, *_):
        filename = askopenfilename()
        self.songs.append(filename)
        
        # показывает/убирает hud в зависимости от положения мыши
    def on_mouse_motion(self, x, y, dx, dy):
        if y < self.height//6:
            self.hud_is_visible = True
        else:
            self.hud_is_visible = False                                        
    
    def switch_sound_bar(self, *_):
        self.sound_bar_is_visible = not self.sound_bar_is_visible
    
    def show_sound_bar(self, *_):
        arcade.draw_lrtb_rectangle_filled(self.width*.968-self.width//100, self.width*.968+self.width//100, self.height//4, self.height//8+self.height//225, arcade.color.GRAY)
        arcade.draw_line(self.width*.968, self.height//7, self.width*.968, self.height//4-self.height//65, arcade.color.WHITE, line_width = 5)
        arcade.draw_line(self.width*.968-self.width//150,self.height//7+self.volume_level, self.width*.968+self.width//150,self.height//7+self.volume_level, arcade.color.WHITE, line_width = 5)
        
    #mouse-press ивенты
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.sound_bar_is_visible:
                if y > self.height//7 and y < self.height//4 - self.height//65:
                    if x > self.width*.968-self.width//125 and x < self.width*.968+self.width//125:
                        self.volume_level = y-self.height//7
                        if self.media_player:
                            self.media_player.volume = self.volume_level/100
                    