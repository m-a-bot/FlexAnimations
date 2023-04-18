import arcade
from settings import *
from Views.Container import ContainerView
from Views.test import TestView
from GUI import GUI
import pyglet
from animations.tornado import Tornado
from animations.wave import Wave

from GUI import GUI

if __name__ == "__main__":
   
    window = arcade.Window(WIDTH, HEIGHT, TITLE, update_rate=1/FPS)

    window.show_view(GUI())

    arcade.run()

