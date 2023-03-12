import arcade
import arcade.gui
from tkinter.filedialog import askopenfilename
class GUI(arcade.View):
    def __init__(self, my_window: arcade.Window, fullscreen = True):
        super().__init__(my_window)
        self.set_location = (0, 0)
        self.width = 1920
        self.height = 1080
        arcade.set_background_color(arcade.color.WENGE) #ставим бэк
        self.paused = True #True, если музыка играет, False, если пауза
        self.hud_is_visible = False #виден ли плеер
        self.sound_bar_is_visible = False #видна ли планка с саундом
        self.volume_level = 50 #уровень громкости
        self.songs = [":resources:music/1918.mp3"]
        self.cur_song_index = 0
        self.media_player = None
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.buttons_array = []
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/"
                                             "play.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                            "play.png")
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                            "pause_square.png")

        # Play/pause button
        self.play_button = arcade.gui.UITextureButton(
            x = self.width//2,
            y = self.height//16,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale = 1.5
        )
        self.play_button.on_click = self.play_button_clicked  # type: ignore                               
        self.buttons_array.append(self.play_button)
        
        
        # Settings button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/gear.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/gear.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/gear.png")

        self.settings = arcade.gui.UITextureButton(
            x = self.width//60,
            y = self.height//16,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale = 1.5
        )
        self.settings.on_click = self.open_settings  # type: ignore                                        
        self.buttons_array.append(self.settings)

        # Star button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/star_square.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/star_square.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/star_square.png")
        self.star = arcade.gui.UITextureButton(
            x = self.width//2-self.width//20,
            y = self.height//16,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale = 1.5
        )
        self.buttons_array.append(self.star)

        # Up button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/up.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png")

        self.up = arcade.gui.UITextureButton(
            x = self.width//2+self.width//20,
            y = self.height//16,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale = .9
        )
        self.up.on_click = self.upload
        self.buttons_array.append(self.up)
        
        
        # Volume button
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")

        # Create our button
        self.volume = arcade.gui.UITextureButton(
            x = self.width*19//20,
            y = self.height//16,
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
            scale = 1.5
        )
        self.buttons_array.append(self.volume)
        self.volume.on_click = self.switch_sound_bar  # type: ignore                                                

        for each in self.buttons_array:
            self.ui_manager.add(each)
        
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
        if y < self.height//6 + 50:
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
                    
