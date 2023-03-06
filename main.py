import arcade
from settings import *
from views.Container import ContainerView


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_WINDOW_TITLE)
    container_view = ContainerView()
    window.show_view(container_view)
    arcade.run()


if __name__ == "__main__":
    main()