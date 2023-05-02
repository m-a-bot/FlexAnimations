import arcade
from settings import *

from GUI import GUI
if __name__ == "__main__":
    window = arcade.Window(WIDTH, HEIGHT, TITLE, update_rate=1/FPS)
    window.show_view(GUI())

    arcade.run()

