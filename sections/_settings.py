import enum
import random
from typing import Iterable, Optional, Union

import imageio as imageio
import scipy
from arcade.application import Window
import numpy
from PIL import Image
from arcade import Sprite, Texture
from arcade.gui.events import UIOnClickEvent

TEXT_COLOR = (238, 20, 223)
WHITE = (255, 255, 255)
PINK = (238, 20, 223)
BLUE = (20, 230, 238)


class Mode(enum.Enum):
    Custom = 1
    Random = 2
    Gradient = 3
    Single = 4


class Type(enum.Enum):
    Random = 1
    Figures = 2
    Lines = 3
    Mixed = 4


ENG = "abcdefghijklmnopqrstuvwxyz"
NUM = "0123456789"


def generate_symbol(symbols=ENG):
    n = len(symbols)

    return symbols[random.randint(0, n-1)]


def generate_string(length: int, symbols=ENG) -> str:
    string_expected = ""

    for i in range(length):
        string_expected += generate_symbol(symbols)

    return string_expected


class Settings:

    def __init__(self):
        self.type: Type = Type.Figures
        self.mode: Mode = None

        self.custom_colors = []
        self.random_colors = []
        self.gradient_colors = []
        self.only_color = None

    def set_mode(self, mode):
        self.mode = mode

    def add_random_colors(self, color1, color2):
        ...

    def add_gradient_colors(self, color1, color2):
        
        self.gradient_colors = [color1, color2]

    def add_only_color(self, color):
        self.only_color = color


from abc import ABC, abstractmethod


class AnimationFactory(ABC):

    def __init__(self, settings: Settings):
        self.settings: Settings = settings

    @abstractmethod
    def create_object(self, template):
        ...

    @abstractmethod
    def update_object(self):
        ...


class SingleColorModeFactory(AnimationFactory):

    def create_object(self, template):

        return self.__create_object_single_color_mode(template, self.settings.only_color)

    def __create_object_single_color_mode(self, template, color):

        _nb = template.copy()

        for i, row in enumerate(template):
            for j, y in enumerate(row):
                if template[i][j][3] != 0:
                    _nb[i][j][:3] = color

        return arcade.Texture(generate_string(50, ENG), image=Image.fromarray(_nb, "RGBA"), hit_box_algorithm = "None")

    def update_object(self):
        ...


class GradientModeFactory(AnimationFactory):

    def create_object(self, template):

        return self.__create_object_gradient_mode(template, *self.settings.gradient_colors)

    def __create_object_gradient_mode(self, template, color1, color2):

        vert = False

        width, height, _ = template.shape

        colors = numpy.round(numpy.linspace(color1, color2, width)) if vert else numpy.round(numpy.linspace(color1, color2, height))

        _nb = template.copy()

        for x in range(0, width):
            for y in range(0, height):
                _nb[x, y, :3] = colors[x if vert else y]

        return arcade.Texture(generate_string(50, ENG), image=Image.fromarray(_nb, "RGBA"), hit_box_algorithm = "None")

    def update_object(self):
        ...


import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from settings import ROOT_DIR
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE1=(0,0,255)


class Check(arcade.gui.UITextureButton):
    texture_unchecked: Texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/unchecked.png")
    texture_checked: Texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/checked.png")
    texture_hovered_unchecked: Texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/unchecked.png")
    texture_hovered_checked: Texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/checked.png")

    checkBoxes = []

    def __init__(self, mode, x: float = 0, y: float = 0, width: float = None, height: float = None, text: str = "",
                 scale: float = None, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, **kwargs):
        self.mode = mode

        super().__init__(x, y, width, height, Check.texture_unchecked, Check.texture_hovered_unchecked, None, text,
                         scale, size_hint, size_hint_min, size_hint_max, style, **kwargs)

        Check.checkBoxes.append(self)

    @classmethod
    def set_all_unchecked(cls):
        for box in cls.checkBoxes:
            box.texture = cls.texture_unchecked
            box.texture_hovered = cls.texture_hovered_unchecked


class Template(arcade.gui.UITextureButton):

    def __init__(self, path_to_image, x: float = 0, y: float = 0, width: float = None, height: float = None,
                 texture: Texture = None, texture_hovered: Texture = None, texture_pressed: Texture = None,
                 text: str = "", scale: float = None, size_hint=None, size_hint_min=None, size_hint_max=None,
                 style=None, **kwargs):
        self.image = path_to_image

        texture: Texture = arcade.load_texture(path_to_image)

        super().__init__(x, y, width, height, texture, texture_hovered, texture_pressed, text, scale, size_hint,
                         size_hint_min, size_hint_max, style, **kwargs)


class SettingsView(arcade.View):

    def __init__(self, main_view):
        super().__init__()
        self.main_view = main_view
        self.bg = arcade.load_texture("resources/icons/фон.png")

        #self.enabled = False

        self.left = 0
        self.bottom = 0
        self.width = self.window.width
        self.height = self.window.height
        self.right = self.width - self.left
        self.top = self.height - self.bottom

        self._settings = Settings()
        self.factory: AnimationFactory = None
        self.single_color_factory = SingleColorModeFactory(self._settings)
        self.gradient_factory = GradientModeFactory(self._settings)

        self.current_mode = None
        self.current_template = None

        self.templates = ["circle.png", "octagon.png", "pentagon.png", "square.png", "star.png", "triangle.png"]

        self.manager = arcade.gui.UIManager(self.window)

        # -------------------
        self.close_btn = arcade.gui.UITextureButton(
            texture=arcade.load_texture("resources/icons/close.png"),
            hover_texture=arcade.load_texture("resources/icons/close.png"),
            press_texture=arcade.load_texture("resources/icons/close.png"),
            scale=1,
            x=self.right - 20,
            y=self.top - 20
        )
        self.manager.add(self.close_btn)
        self.close_btn.on_click = self.close_btn_on_click

        self.apply_button = arcade.gui.UITextureButton(
            texture=arcade.load_texture("resources/icons/Подтвердить.png"),
            hover_texture=arcade.load_texture("resources/icons/Подтвердить.png"),
            press_texture=arcade.load_texture("resources/icons/Подтвердить.png"),
            scale=1,
            x=(self.right + self.left) // 2 - 125,
            y=self.bottom + 20
        )
        self.apply_button.available = False
        self.manager.add(self.apply_button)
        self.apply_button.on_click = self.apply_button_on_click
        # ------------------

        padding = 40
        self.llayout = arcade.gui.UILayout(self.left + padding, self.bottom,
                                           self.width * 4 // 10 - padding, self.height)

        self.rlayout = arcade.gui.UILayout(self.left + self.width * 4 // 10 + padding, self.bottom,
                                           self.width // 2 + self.width//10 - padding, self.height)

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=self.llayout.height // 12, align="left")

        layout.add(self.check_box(Mode.Custom, "Кастомный"))
        layout.add(self.check_box(Mode.Random, "Случайный"))
        layout.add(self.check_box(Mode.Gradient, "Градиент"))
        layout.add(self.check_box(Mode.Single, "Однотонный"))

        temp1 = arcade.gui.UIBoxLayout(vertical=False, space_between=self.llayout.width // 5)
        temp2 = arcade.gui.UIBoxLayout(vertical=False, space_between=self.llayout.width // 5)

        for i in range(3):
            tp = Template(ROOT_DIR + r"/resources/icons/templates/" + self.templates[i], scale=0.5)
            tp.on_click = self.image_clicked
            temp1.add(tp.with_space_around(2, 2, 2, 2, BLUE))

        for i in range(3, 6):
            tp = Template(ROOT_DIR + r"/resources/icons/templates/" + self.templates[i], scale=0.5)
            tp.on_click = self.image_clicked
            temp2.add(tp.with_space_around(2, 2, 2, 2, BLUE))

        self.llayout.add(arcade.gui.UIAnchorWidget(child=temp1, anchor_y="bottom", align_y=180))
        self.llayout.add(arcade.gui.UIAnchorWidget(child=temp2, anchor_y="bottom", align_y=90))

        self.llayout.add(
            arcade.gui.UIAnchorWidget(child=layout, anchor_x="left", align_x=50, anchor_y="top", align_y=-65))

        self.r_group1 = None
        self.g_group1 = None
        self.b_group1 = None
        self.picture1 = None
        self.group1 = None

        self.r_group2 = None
        self.g_group2 = None
        self.b_group2 = None
        self.picture2 = None
        self.group2 = None

        self.result_group = arcade.gui.UIBoxLayout(space_between=10)

        self.result_group.add(arcade.gui.UILabel(text="Результат"))

        self.result_texture = None

        self.rlayout.add(child=arcade.gui.UIAnchorWidget(child=self.result_group, align_y=-65))

        self.manager.add(self.llayout)  # .with_space_around(padding, padding, padding, padding, PINK))
        self.manager.add(self.rlayout)  # .with_space_around(padding, padding, padding, padding, WHITE))

    def manipulate_color(self, number):

        group = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        block1 = arcade.gui.UIBoxLayout(space_between=16)
        block1.add(arcade.gui.UILabel(text="R"))
        block1.add(arcade.gui.UILabel(text="G"))
        block1.add(arcade.gui.UILabel(text="B"))
        group.add(block1)

        block = arcade.gui.UIBoxLayout(space_between=8)

        self.add_slider_with_different_variables(number)

        block.add(self.r_group1 if number == 1 else self.r_group2)
        block.add(self.g_group1 if number == 1 else self.g_group2)
        block.add(self.b_group1 if number == 1 else self.b_group2)

        group.add(block)

        self.add_picture_with_different_variables(number)

        group.add(self.picture1 if number == 1 else self.picture2)

        return group

    def add_slider_with_different_variables(self, number):

        if number == 1:
            self.r_group1 = UISlider(min_value=0, max_value=255, width=200, height=40, style={
                "normal_filled_bar": RED, 
                "hovered_filled_bar":RED,
                "pressed_filled_bar":RED})
            self.g_group1 = UISlider(min_value=0, max_value=255, width=200, height=40,style={
                "normal_filled_bar": GREEN, 
                "hovered_filled_bar":GREEN,
                "pressed_filled_bar":GREEN})
            self.b_group1 = UISlider(min_value=0, max_value=255, width=200, height=40,style={
                "normal_filled_bar": BLUE1, 
                "hovered_filled_bar":BLUE1,
                "pressed_filled_bar":BLUE1})

        else:
            self.r_group2 = UISlider(min_value=0, max_value=255, width=200, height=40, style={
                "normal_filled_bar": RED, 
                "hovered_filled_bar":RED,
                "pressed_filled_bar":RED})
            self.g_group2 = UISlider(min_value=0, max_value=255, width=200, height=40,style={
                "normal_filled_bar": GREEN, 
                "hovered_filled_bar":GREEN,
                "pressed_filled_bar":GREEN})
            self.b_group2 = UISlider(min_value=0, max_value=255, width=200, height=40,style={
                "normal_filled_bar": BLUE1, 
                "hovered_filled_bar":BLUE1,
                "pressed_filled_bar":BLUE1})

    def add_picture_with_different_variables(self, number):

        if number == 1:
            self.picture1 = arcade.gui.UIDummy(color=(self.r_group1.value, self.g_group1.value, self.b_group1.value))
        else:
            self.picture2 = arcade.gui.UIDummy(color=(self.r_group2.value, self.g_group2.value, self.b_group2.value))

    def update(self, delta_time: float):

        if self.current_mode == Mode.Gradient:

            new_colors = [(self.r_group1.value, self.g_group1.value, self.b_group1.value), (self.r_group2.value, self.g_group2.value, self.b_group2.value)]

            if self._settings.gradient_colors != new_colors:
                self._settings.add_gradient_colors(*new_colors)

            if self.current_template is not None:
                self.result_texture = self.factory.create_object(self.current_template)

        if self.current_mode == Mode.Single:
            new_color = (self.r_group1.value, self.g_group1.value, self.b_group1.value)
            if self._settings.only_color != new_color:
                self._settings.add_only_color(new_color)

            if self.current_template is not None:
                self.result_texture = self.factory.create_object(self.current_template)

        if self.picture1:
            self.picture1.color = (self.r_group1.value, self.g_group1.value, self.b_group1.value)

        if self.picture2:
            self.picture2.color = (self.r_group2.value, self.g_group2.value, self.b_group2.value)

    def check_box(self, mode, text):

        layout = arcade.gui.UIBoxLayout(vertical=False, space_between=25)

        check_b = Check(mode, scale=0.4)

        check_b.on_click = self.handler_checkbox

        layout.add(check_b)

        layout.add(arcade.gui.UILabel(text=text, align="center", text_color=WHITE))

        return layout

    def image_clicked(self, event: UIOnClickEvent):

        obj = event.source

        img = imageio.imread(obj.image, mode='RGBA')

        self.current_template = img

    def handler_checkbox(self, event: UIOnClickEvent):

        Check.set_all_unchecked()

        obj = event.source

        obj.texture = Check.texture_checked
        obj.texture_hovered = Check.texture_hovered_checked

        try:
            self.rlayout.remove(self.group1)
        except:
            ...

        try:
            if self.group2:
                self.rlayout.remove(self.group2)
        except:
            ...

        self.group1 = arcade.gui.UIAnchorWidget(child=self.manipulate_color(1), anchor_y="top", align_y=-50)
        self.group2 = arcade.gui.UIAnchorWidget(child=self.manipulate_color(2), align_y=75)

        self.current_mode = obj.mode

        if obj.mode == Mode.Random:
            self.rlayout.add(self.group1)
            self.rlayout.add(self.group2)

        if obj.mode == Mode.Gradient:
            self.rlayout.add(self.group1)
            self.rlayout.add(self.group2)

        self.factory = self.gradient_factory

        if obj.mode == Mode.Single:
            self.rlayout.add(self.group1)

            self.factory = self.single_color_factory

    def on_draw(self):
        
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.bg)

        if self.result_texture is not None:

            self.result_texture.draw_scaled(self.width*3//4, self.height//5, scale=1)

        self.manager.enable()
        self.manager.draw()


    def apply_button_on_click(self, *_):

        if self.result_texture is None:
            return

        self.main_view.rebase_gui_sprites_texture(self.result_texture)

        self.window.show_view(self.main_view)
        

    def close_btn_on_click(self, *_):

        self.window.show_view(self.main_view)
