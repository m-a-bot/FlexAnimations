import arcade
from settings import *
from views.Container import ContainerView
from views.test import TestView
from GUI import GUI
import pyglet
from animations.tornado import Tornado
from animations.wave import Wave

from GUI import GUI

if __name__ == "__main__":
   
    window = arcade.Window(1920, 1080, TITLE, update_rate=1/FPS)

    window.show_view(GUI())

    arcade.run()

