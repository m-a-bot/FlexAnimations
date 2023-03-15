import arcade
from settings import *
from views.Container import ContainerView
from views.test import TestView
from GUI import GUI
import pyglet

from GUI import GUI

if __name__ == "__main__":
   
    window = arcade.Window(WIDTH, HEIGHT, TITLE)

    window.show_view(GUI())

    arcade.run()

