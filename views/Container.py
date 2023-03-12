import arcade
import numpy
import numpy.random
from assets.MovementSprite import MovementSprite

class ContainerView(arcade.View):

    def __init__(self):

        super().__init__()
        
        self.add_figures()
        
        self.bg = arcade.load_texture(":resources:images/backgrounds/stars.png")

    def add_figures(self):
        self.figures = arcade.SpriteList()

        x = [-3, -1, 1, 3]
        y = [-3, -2, 2, 3]

        scales = [0.6, 1, 1.1, 0.7, 1.3, 0.9]

        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:onscreen_controls/shaded_light/wrench.png",
                                           center_x=200,
                                           center_y=100,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:onscreen_controls/shaded_light/select.png",
                                           center_x=100,
                                           center_y=200,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/cards/cardSpadesJ.png",
                                           center_x=150,
                                           center_y=150,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/cards/cardHearts3.png",
                                           center_x=300,
                                           center_y=300,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y),
                                           texture=arcade.make_circle_texture(60, arcade.color_from_hex_string("#123fdc")),
                                           center_x=330,
                                           center_y=250,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y),
                                           texture=arcade.make_soft_square_texture(90, arcade.color_from_hex_string("#123fdc")),
                                           center_x=250,
                                           center_y=120,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/space_shooter/meteorGrey_big1.png",
                                           center_x=300,
                                           center_y=300,
                                           scale=numpy.random.choice(scales)))
        
        self.figures.append(MovementSprite(numpy.random.choice(x),numpy.random.choice(y), filename=":resources:images/test_textures/xy_square.png",
                                           center_x=500,
                                           center_y=100,
                                           scale=numpy.random.choice(scales)))


    def on_update(self, delta_time: float):
        # count_figures = len(self.figures)
        # for i in range(count_figures-1):
        #     for j in range(1, count_figures):
        #         if arcade.check_for_collision(self.figures[i], self.figures[j]):
        #             self.figures[i].strafe()

        self.figures.update()


    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,self.window.width, self.window.height, self.bg)
        self.figures.draw()

        

