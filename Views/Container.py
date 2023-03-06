import arcade

WIDTH, HEIGHT = 800, 600 



class ContainerView(arcade.View):
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        
        arcade.draw_xywh_rectangle_outline(WIDTH/2, HEIGHT/2, 80, 80, (200, 20, 90))

        arcade.draw_triangle_outline(WIDTH/6, HEIGHT/6, WIDTH/6 + 80, HEIGHT/6, WIDTH/6 + 40, HEIGHT/6 + 80,
                                     (155,89,90))