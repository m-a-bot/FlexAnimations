import arcade




class ContainerView(arcade.View):

    def __init__(self):

        super().__init__()
        

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#BABAB4"))


    def on_draw(self):

        arcade.start_render()

