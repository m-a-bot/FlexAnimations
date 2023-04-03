import arcade
import numpy
import numpy.random
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

class MovementSprite:

    def __init__(self, *_) -> None:
        pass

class ContainerView(arcade.View):

    def __init__(self):

        ...


    def setup(self):
        ...

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

