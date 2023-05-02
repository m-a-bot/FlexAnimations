import enum
from typing import Iterable, Optional, Union
from .menu import Buttons
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


class Settings:

    def __init__(self):

        self.type: Type = Type.Figures
        self.mode: Mode = None

        self.custom_colors = []
        self.random_colors = []
        self.gradient_colors = []
        self.only_color = None


from abc import ABC, abstractmethod
class AnimationFactory(ABC):


    def __init__(self, settings: Settings):
        
        self.settings: Settings = settings


    @abstractmethod
    def create_object():
        ...


    @abstractmethod
    def update_object():
        ...


import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from settings import ROOT_DIR

class Check(arcade.gui.UITextureButton):

    texture_unchecked: Texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/unchecked.png")
    texture_checked: Texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/checked.png") 
    texture_hovered_unchecked: Texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/unchecked.png")
    texture_hovered_checked: Texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/checked.png")


    checkBoxes = []

    def __init__(self, mode, x: float = 0, y: float = 0, width: float = None, height: float = None, text: str = "", scale: float = None, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, **kwargs):
        
        self.mode = mode

        super().__init__(x, y, width, height, Check.texture_unchecked, Check.texture_hovered_unchecked, None, text, scale, size_hint, size_hint_min, size_hint_max, style, **kwargs)

        Check.checkBoxes.append(self)


    def on_click(self, event: UIOnClickEvent):
        
        Check.set_all_unchecked()
        
        self.texture = Check.texture_checked
        self.texture_hovered = Check.texture_hovered_checked

        if self.mode == Mode.Single:
            ...


    @classmethod
    def set_all_unchecked(cls):
        
        for box in cls.checkBoxes:
            box.texture = cls.texture_unchecked
            box.texture_hovered = cls.texture_hovered_unchecked


def check_box(mode, text):

    layout = arcade.gui.UIBoxLayout(vertical=False, space_between=25)

    layout.add(Check(mode, scale=0.4))

    layout.add(arcade.gui.UILabel(text=text, align="center", text_color=WHITE))

    return layout


class Template(arcade.gui.UITextureButton):

    def __init__(self, path_to_image, x: float = 0, y: float = 0, width: float = None, height: float = None, texture: Texture = None, texture_hovered: Texture = None, texture_pressed: Texture = None, text: str = "", scale: float = None, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, **kwargs):
        
        self.image = path_to_image
        
        texture: Texture = arcade.load_texture(path_to_image)
        
        super().__init__(x, y, width, height, texture, texture_hovered, texture_pressed, text, scale, size_hint, size_hint_min, size_hint_max, style, **kwargs)


    def on_click(self, event: UIOnClickEvent):
        ...

class SettingsSection(arcade.Section):


    def __init__(self, left: int, bottom: int, width: int, height: int, *, name: str | None = None, accept_keyboard_events: bool | Iterable = True, prevent_dispatch: Iterable | None = None, prevent_dispatch_view: Iterable | None = None, local_mouse_coordinates: bool = False, enabled: bool = True, modal: bool = False):
        super().__init__(left, bottom, width, height, name=name, accept_keyboard_events=accept_keyboard_events, prevent_dispatch=prevent_dispatch, prevent_dispatch_view=prevent_dispatch_view, local_mouse_coordinates=local_mouse_coordinates, enabled=enabled, modal=modal)

        self.enabled = False
        self.factory: AnimationFactory = None

        self.templates = ["circle.png", "octagon.png", "pentagon.png", "square.png", "star.png", "triangle.png"]

        self.manager = arcade.gui.UIManager(self.window)

        # -------------------
        self.close_btn = arcade.gui.UITextureButton(
            texture=arcade.load_texture("resources/icons/close.png"),
            hover_texture=arcade.load_texture("resources/icons/close.png"),
            press_texture=arcade.load_texture("resources/icons/close.png"),
            scale=1,
            x=self.right -20,
            y=self.top
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
        #self.apply_button.on_click = self.apply_button_on_click
        # ------------------

        padding = 25
        llayout = arcade.gui.UILayout(self.left, self.bottom, 
                                      self.width//3, self.height)
        
        
        rlayout = arcade.gui.UILayout(self.left + self.width//3, self.bottom, 
                                      self.width * 2 // 3, self.height)
        
        

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=llayout.height//12, align="left")

        layout.add(check_box(Mode.Custom, "Кастомный"))
        layout.add(check_box(Mode.Random, "Случайный"))
        layout.add(check_box(Mode.Gradient, "Градиент"))
        layout.add(check_box(Mode.Single, "Однотонный"))

        temp1 = arcade.gui.UIBoxLayout(vertical=False, space_between=llayout.width//5)
        temp2 = arcade.gui.UIBoxLayout(vertical=False, space_between=llayout.width//5)

        for i in range(3):
            temp1.add(Template(ROOT_DIR + r"/resources/icons/templates/" + self.templates[i], scale=0.1).with_space_around(2, 2, 2, 2, BLUE))

        for i in range(3, 6):
            temp2.add(Template(ROOT_DIR + r"/resources/icons/templates/" + self.templates[i], scale=0.1).with_space_around(2, 2, 2, 2, BLUE))
        
        llayout.add(arcade.gui.UIAnchorWidget(child=temp1, anchor_y="bottom", align_y=180))
        llayout.add(arcade.gui.UIAnchorWidget(child=temp2, anchor_y="bottom", align_y=90))

        llayout.add(arcade.gui.UIAnchorWidget(child=layout, anchor_x="left", align_x=25, anchor_y="top", align_y=-25))


        self.single = arcade.gui.UIBoxLayout(vertical=False)

        block = arcade.gui.UIBoxLayout()

        self.r_single = UISlider(min_value=0, max_value=255, width=200, height=40)
        self.g_single = UISlider(min_value=0, max_value=255, width=200, height=40)
        self.b_single = UISlider(min_value=0, max_value=255, width=200, height=40)

        block.add(self.r_single)
        block.add(self.g_single)
        block.add(self.b_single)

        self.single.add(arcade.gui.UIAnchorWidget(child=block))

        rlayout.add(self.single)

        self.manager.add(llayout)#.with_space_around(padding, padding, padding, padding, PINK))
        self.manager.add(rlayout)#.with_space_around(padding, padding, padding, padding, WHITE))


    def on_draw(self):
        
        arcade.draw_xywh_rectangle_filled(self.left, self.bottom, self.width, self.height, (50, 50, 50, 200))

        self.manager.enable()
        self.manager.draw()


    def close_btn_on_click(self, *_):
        self.enabled = False


    