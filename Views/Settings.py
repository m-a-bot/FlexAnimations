from typing import Optional
import arcade
import arcade.gui

SIZE_BUTTON = 40

class SettingsView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()

        layout = arcade.gui.UILayout(0,0,self.window.width, self.window.height)

        layout.add(
            arcade.gui.UIAnchorWidget(child=arcade.gui.UIBoxLayout(
            text="Настройки",
            font_size=26,
            text_color=arcade.color_from_hex_string("#000"),
            align="center"
            ), anchor_y="left")
        )

        __texture: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/flat_dark/close.png")
        __texture_shared: Optional[arcade.texture.Texture] = arcade.load_texture(":resources:onscreen_controls/shaded_dark/close.png") 

        self.btn_close_view = arcade.gui.UITextureButton(
            width=SIZE_BUTTON,
            height=SIZE_BUTTON,
            texture=__texture,
            texture_hovered = __texture_shared,
            texture_pressed = __texture_shared,
        )
        self.btn_close_view.on_click = self.btn_close_clicked

        layout.add(
            arcade.gui.UIAnchorWidget(
            child=self.btn_close_view,
            anchor_y="right",
            anchor_x="right")
        )


    def on_draw(self):
        arcade.start_render()


    def btn_close_clicked(self):
        view = ContainerView()
        self.window.show_view(view)