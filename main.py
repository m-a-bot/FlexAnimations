import arcade
from Views.Container import ContainerView

def main():
    window = arcade.Window(800, 600, "2d animation")
    container_view = ContainerView()
    window.show_view(container_view)
    arcade.run()


if __name__ == "__main__":
    main()