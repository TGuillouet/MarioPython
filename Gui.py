import arcade


class GuiElement:
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 align="center"):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.align = align

    def draw(self):
        arcade.draw_text(self.text, self.center_x, self.center_y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align=self.align,
                         anchor_x="center", anchor_y="center")

    def draw_new_text(self, new_text=''):
        arcade.draw_text(str(new_text), self.center_x, self.center_y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align=self.align,
                         anchor_x="center", anchor_y="center")
