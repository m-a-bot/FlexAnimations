import arcade
from arcade import SpriteSolidColor, SpriteList


class Menu(arcade.Section):

    def __init__(self, left, bottom, width, height):
        super().__init__(left, bottom, width, height, modal=True)

        self.enabled = False
        
        self.gui_elements = SpriteList()

        self.available_area = [self.left + 0, self.bottom + 100, self.width, self.height]
        self.shift = (self.height - 250) / 4
        
        self.back_button = SpriteSolidColor(100, 50, (0, 0, 177, 180))
        self.back_button.set_position(self.left + self.width / 2, self.bottom + 50)

        self.gui_elements.append(self.back_button)

    def on_draw(self):

        arcade.draw_xywh_rectangle_filled(*self.available_area, (50, 50, 50, 200))
        
        self.gui_elements.draw()

        arcade.draw_text("Режим анимации", self.left + 50, self.top - self.shift, font_size=20, bold=True)

        arcade.draw_text("Цвет анимации",self.left + 50, self.top - 2 * self.shift, font_size=20, bold=True)

        arcade.draw_text("Фигуры",self.left + 50, self.top - 3 * self.shift, font_size=20, bold=True)

        arcade.draw_text("Контейнер",self.left + 50, self.top - 4 * self.shift, font_size=20, bold=True)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.back_button.collides_with_point((x, y)):
                self.enabled = False
