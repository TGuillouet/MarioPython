import arcade
import random

SPRITE_SCALE = 2


class Coin(arcade.AnimatedTimeSprite):
    def __init__(self, center_x=0, center_y=0, width=16, height=16):
        super().__init__()
        self.center_x = center_x * SPRITE_SCALE * width
        self.center_y = center_y * SPRITE_SCALE * height
        print(self.center_x)

        self.textures = []
        self.textures.append(arcade.load_texture("Sprites/coin.png", scale=SPRITE_SCALE))
        self.textures.append(arcade.load_texture("Sprites/coin_01.png", scale=SPRITE_SCALE))
        self.cur_texture_index = random.randrange(len(self.textures))