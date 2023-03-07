import arcade
from sections.player import PlayerSection
from sections.canvas import CanvasSection
from sections.volume_slider1 import ModalSection


class ContainerView(arcade.View):

    def __init__(self):

        super().__init__()

        self.player = PlayerSection(0, 0, 
                                    self.window.width, 80)
        
        self.canvas = CanvasSection(0, self.player.top, self.window.width, self.window.height)

        # self.volume_slider = ModalSection(self.window.width - 60, self.player.height//2, 60, 60)

        # add the sections
        # self.section_manager.add_section(self.volume_slider)
        self.section_manager.add_section(self.player)
        self.section_manager.add_section(self.canvas)
        


    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#BABAB4"))


    def on_draw(self):
        arcade.start_render()