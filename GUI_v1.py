import arcade

class AppWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen = False)
        self.set_location = (0, 0)
        arcade.set_background_color(arcade.color.WENGE) #ставим бэк
        self.play_pause = True #True, если музыка играет, False, если пауза
        self.hud_is_visible = True #виден ли плеер
        self.sound_bar_is_visible = False #видна ли планка с саундом
        self.sound_level = 0 #уровень громкости
    
    #ебашит hud (плеер)
    def on_draw(self):
        arcade.start_render()
        if self.hud_is_visible or self.sound_bar_is_visible:
            arcade.draw_line(0, self.height//12, self.width, self.height//12, arcade.color.ALMOND, line_width = self.height//6)
            arcade.draw_line(0, self.height//6, self.width, self.height//6, arcade.color.BLACK, line_width = 5)
            arcade.draw_lrtb_rectangle_filled(self.width//20, self.width//20+self.width//20, self.height//12+self.height//18, self.height//12-self.height//25, arcade.color.BLACK)
            arcade.draw_lrtb_rectangle_filled(self.width//2-self.width//40, self.width//2+self.width//40, self.height//12+self.height//18, self.height//12-self.height//25, arcade.color.BLACK)
            arcade.draw_lrtb_rectangle_filled(self.width//2-self.width//10, self.width//2-self.width//10+self.width//20, self.height//12+self.height//18, self.height//12-self.height//25, arcade.color.BLACK)
            arcade.draw_circle_filled(self.width//2+self.width//14, self.height//11, self.height//20, arcade.color.BLACK)
            arcade.draw_lrtb_rectangle_filled(self.width*.9, self.width*.9+self.width//20, self.height//12+self.height//18, self.height//12-self.height//25, arcade.color.BLACK)
            self.draw_play_or_pause_button()
            if self.sound_bar_is_visible:
                self.show_sound_bar()
        
    #при нажатии на пробел или по тыку кнопки меняет pause/play
    def draw_play_or_pause_button(self):
        if self.play_pause:
            arcade.draw_triangle_filled(self.width//2-self.width//60, self.height//11+self.height//30, self.width//2-self.width//60, self.height//11-self.height//30, self.width//2+self.width//60, self.height//11, arcade.color.WHITE)
        else:
            arcade.draw_line(self.width//2-self.width//90, self.height//13+self.height//18, self.width//2-self.width//90, self.height//13-self.height//40, arcade.color.WHITE, line_width = 10)
            arcade.draw_line(self.width//2+self.width//90, self.height//13+self.height//18, self.width//2+self.width//90, self.height//13-self.height//40, arcade.color.WHITE, line_width = 10)
            
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            self.play_pause = not self.play_pause
            self.draw_play_or_pause_button()
        
    #показывает/убирает hud в зависимости от положения мыши
    def on_mouse_motion(self, x, y, dx, dy):
        if y > self.height//6:
            self.hud_is_visible = False
        else:
            self.hud_is_visible = True
    
    def show_sound_bar(self):
        arcade.draw_lrtb_rectangle_filled(self.width*.9+self.width//60, self.width*.9+self.width//30, self.height//4, self.height//8, arcade.color.BLACK)
        arcade.draw_line(self.width*.9+self.width//40, self.height//7, self.width*.9+self.width//40, self.height//4-self.height//65, arcade.color.WHITE, line_width = 5)
        arcade.draw_line(self.width*.9+self.width//50,(self.height//4-self.height//65-self.height//7)/2+self.height//7+self.sound_level, self.width*.9+self.width//33,(self.height//4-self.height//65-self.height//7)/2+self.height//7+self.sound_level, arcade.color.WHITE, line_width = 5)
        
    #mouse-press ивенты
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if y > self.height//12-self.height//25 and y < self.height//12+self.height//18:
                if x > self.width//20 and x < self.width//20+self.width//20:
                    ... #activates when left button is pressed
                    
                elif x > self.width//2-self.width//10 and x < self.width//2-self.width//10+self.width//20:
                    ... #activates when middle left button is pressed
                    
                elif x > self.width//2-self.width//40 and x < self.width//2+self.width//40:
                    #activates when the middle button is pressed
                    self.play_pause = not self.play_pause
                    self.draw_play_or_pause_button()
                    
                elif x > self.width//2+self.width//14+self.height//20 and x < self.width//2+self.width//14-self.height//20:
                    ... #activates when circle button is pressed
                    
                elif x > self.width*.9 and x < self.width*.9+self.width//20:
                    self.sound_bar_is_visible = not self.sound_bar_is_visible
                    self.show_sound_bar() #sound button
            if y > self.height//7 and y < self.height//4 - self.height//65:
                if x > self.width*.9+self.width//60 and x < self.width*.9+self.width//30:
                    self.sound_level = y-self.height//7-50
                    self.show_sound_bar()
                    
                    
                    
        
AppWindow(1920, 1080, 'App')
arcade.run()


