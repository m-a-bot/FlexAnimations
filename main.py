import arcade
from settings import *
from views.Container import ContainerView
from views.test import TestView
from .GUI import GUI

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE, resizable=False)

    container_view = ContainerView()
    window.show_view(container_view)
    arcade.run()


if __name__ == "__main__":
    main()