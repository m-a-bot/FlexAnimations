import arcade

class ModalSection(arcade.Section):
    """ A modal section that represents a popup that waits for user input """

    def __init__(self, left: int, bottom: int, width: int, height: int):
        super().__init__(left, bottom, width, height, modal=True, enabled=False)

        # modal button
        self.button = arcade.SpriteSolidColor(100, 50, arcade.color.RED)
        pos = self.left + self.width / 2, self.bottom + self.height / 2
        self.button.position = pos

    def on_draw(self):
        # draw modal frame and button
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top,
                                          self.bottom, arcade.color.GRAY)
        arcade.draw_lrtb_rectangle_outline(self.left, self.right, self.top,
                                           self.bottom, arcade.color.WHITE)
        self.draw_button()

    def draw_button(self):
        # draws the button and button text
        self.button.draw()
        arcade.draw_text('Close Modal', self.button.left + 5,
                         self.button.bottom + self.button.height / 2,
                         arcade.color.WHITE)

    def on_resize(self, width: int, height: int):
        """ set position on screen resize """
        self.left = width // 3
        self.bottom = (height // 2) - self.height // 2
        pos = self.left + self.width / 2, self.bottom + self.height / 2
        self.button.position = pos

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Check if the button is pressed """
        if self.button.collides_with_point((x, y)):
            self.enabled = False