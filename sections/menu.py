import arcade
from arcade import SpriteSolidColor, SpriteList
from animations.tornado import Tornado
from animations.wave import Wave
from animations.confusion import Chaos
from animations.animation import FiguresType


class Buttons(arcade.View):
    def add_texture_button(texture_file_name: str,
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


class Menu(arcade.Section):

    def __init__(self, left, bottom, width, height):
        super().__init__(left, bottom, width, height, modal=True)

        self.enabled = False

        self.figure = FiguresType

        self.gui_elements = SpriteList()

        self.gui_sprites = SpriteList()
        self.gui_animation = None

        self.available_area = [self.left + 0, self.bottom + 100, self.width, self.height]
        self.shift = (self.height - 250) / 4

        self.back_button = SpriteSolidColor(100, 50, (0, 0, 177, 180))
        self.back_button.set_position(self.left + self.width / 2, self.bottom + 50)

        self.gui_elements.append(self.back_button)

        self.animation_buttons_manager = arcade.gui.UIManager(self.window)

        self.btn_diff = self.height // 5

        self.first_animation_mode_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/Кнопка-Торнадо.png",
            hover_texture_file_name="resources/icons/Кнопка-Торнадо.png",
            press_texture_file_name="resources/icons/Кнопка-Торнадо.png",
            _scale=1,
            _x=self.left + 250,
            _y=self.top - self.btn_diff
        )
        self.animation_buttons_manager.add(self.first_animation_mode_btn)
        self.first_animation_mode_btn.on_click = self.first_animation_btn_on_click

        self.second_animation_mode_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/Кнопка-Волна.png",
            hover_texture_file_name="resources/icons/Кнопка-Волна.png",
            press_texture_file_name="resources/icons/Кнопка-Волна.png",
            _scale=1,
            _x=self.left + 250,
            _y=self.top - 2 * self.btn_diff
        )
        self.animation_buttons_manager.add(self.second_animation_mode_btn)
        self.second_animation_mode_btn.on_click = self.second_animation_btn_on_click

        self.third_animation_mode_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/Кнопка-Хаос.png",
            hover_texture_file_name="resources/icons/Кнопка-Хаос.png",
            press_texture_file_name="resources/icons/Кнопка-Хаос.png",
            _scale=1,
            _x=self.left + 250,
            _y=self.top - 3 * self.btn_diff
        )
        self.animation_buttons_manager.add(self.third_animation_mode_btn)
        self.third_animation_mode_btn.on_click = self.third_animation_btn_on_click

        self.first_figure_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/Кнопка-Круг.png",
            hover_texture_file_name="resources/icons/Кнопка-Круг.png",
            press_texture_file_name="resources/icons/Кнопка-Круг.png",
            _scale=1,
            _x=self.right - 350,
            _y=self.top - self.btn_diff
        )
        self.animation_buttons_manager.add(self.first_figure_btn)
        self.first_figure_btn.on_click = self.first_figure_btn_on_click

        self.second_figure_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/Кнопка-Треугольник.png",
            hover_texture_file_name="resources/icons/Кнопка-Треугольник.png",
            press_texture_file_name="resources/icons/Кнопка-Треугольник.png",
            _scale=1,
            _x=self.right - 350,
            _y=self.top - 2 * self.btn_diff
        )
        self.animation_buttons_manager.add(self.second_figure_btn)
        self.second_figure_btn.on_click = self.second_figure_btn_on_click

        self.third_figure_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/Кнопка-Квадрат.png",
            hover_texture_file_name="resources/icons/Кнопка-Квадрат.png",
            press_texture_file_name="resources/icons/Кнопка-Квадрат.png",
            _scale=1,
            _x=self.right - 350,
            _y=self.top - 3 * self.btn_diff
        )
        self.animation_buttons_manager.add(self.third_figure_btn)
        self.third_figure_btn.on_click = self.third_figure_btn_on_click

        self.close_btn = Buttons.add_texture_button(
            texture_file_name="resources/icons/close.png",
            hover_texture_file_name="resources/icons/close.png",
            press_texture_file_name="resources/icons/close.png",
            _scale=1,
            _x=self.right -20,
            _y=self.top+80
        )
        self.animation_buttons_manager.add(self.close_btn)
        self.close_btn.on_click = self.close_btn_on_click

        self.apply_button = Buttons.add_texture_button(
            texture_file_name="resources/icons/Подтвердить.png",
            hover_texture_file_name="resources/icons/Подтвердить.png",
            press_texture_file_name="resources/icons/Подтвердить.png",
            _scale=1,
            _x=(self.right + self.left) // 2 - 125,
            _y=self.bottom + 100
        )
        self.apply_button.available = False
        self.animation_buttons_manager.add(self.apply_button)
        self.apply_button.on_click = self.apply_button_on_click

        self.remove_all_animations = Buttons.add_texture_button(
            texture_file_name="resources/icons/Убрать.png",
            hover_texture_file_name="resources/icons/Убрать.png",
            press_texture_file_name="resources/icons/Убрать.png",
            _scale=.9,
            _x=self.left+250,
            _y=self.top - 3.7 * self.btn_diff
        )
        self.animation_buttons_manager.add(self.remove_all_animations)
        self.remove_all_animations.on_click = self.remove_all_animations_on_click
    def on_draw(self):

        arcade.draw_xywh_rectangle_filled(*self.available_area, (50, 50, 50, 200))
        arcade.draw_xywh_rectangle_filled(self.left, self.top+80, self.right-self.left, 20, arcade.color.BLACK)
        arcade.draw_text('Настройки', self.left, self.top +80)
        self.animation_buttons_manager.enable()
        self.animation_buttons_manager.draw()
        self.gui_elements.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.back_button.collides_with_point((x, y)):
                self.enabled = False

    def first_animation_btn_on_click(self, *_):
        self.pre_animation = Tornado
        try:
            if self.pre_animation is None or self.pre_figure is None:
                self.apply_button.available = False
            else:
                self.apply_button.available = True
        except AttributeError:
            self.apply_button.available = False

    def second_animation_btn_on_click(self, *_):
        self.pre_animation = Wave
        try:
            if self.pre_animation is None or self.pre_figure is None:
                self.apply_button.available = False
            else:
                self.apply_button.available = True
        except AttributeError:
            self.apply_button.available = False

    def third_animation_btn_on_click(self, *_):
        self.pre_animation = Chaos
        try:
            if self.pre_animation is None or self.pre_figure is None:
                self.apply_button.available = False
            else:
                self.apply_button.available = True
        except AttributeError:
            self.apply_button.available = False

    def first_figure_btn_on_click(self, *_):
        self.pre_figure = FiguresType.CIRCLE
        try:
            if self.pre_animation is None or self.pre_figure is None:
                self.apply_button.available = False
            else:
                self.apply_button.available = True
        except AttributeError:
            self.apply_button.available = False

    def second_figure_btn_on_click(self, *_):
        self.pre_figure = FiguresType.TRIANGLE
        try:
            if self.pre_animation is None or self.pre_figure is None:
                self.apply_button.available = False
            else:
                self.apply_button.available = True
        except AttributeError:
            self.apply_button.available = False

    def third_figure_btn_on_click(self, *_):
        self.pre_figure = FiguresType.SQUARE
        try:
            if self.pre_animation is None or self.pre_figure is None:
                self.apply_button.available = False
            else:
                self.apply_button.available = True
        except AttributeError:
            self.apply_button.available = False

    def remove_all_animations_on_click(self, *_):
        self.gui_sprites.clear()
        self.gui_animation = None

    def close_btn_on_click(self, *_):
        self.enabled = False

    def apply_button_on_click(self, *_):
        if self.apply_button.available:
            self.gui_animation = self.pre_animation(self.pre_figure)
            self.gui_animation.fill_sprites(self.gui_sprites)
            self.figure = self.pre_figure
            self.enabled = False
