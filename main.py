import arcade
from settings import *
from views.Container import ContainerView
from views.test import TestView
from GUI import GUI
import pyglet

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE, resizable=True)

    container_view = ContainerView()
    window.show_view(container_view)

    arcade.run()


if __name__ == "__main__":
    # main()

    window = arcade.Window(WIDTH, HEIGHT, TITLE)

    window.show_view(GUI(window))

    arcade.run()