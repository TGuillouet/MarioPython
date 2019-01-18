import arcade
import random
from Consts import SPRITE_SCALE


class Coin(arcade.AnimatedTimeSprite):
    def __init__(self, center_x=0, center_y=0, width=16, height=16):
        """Create a coin with an animation"""
        super().__init__()
        self.center_x = center_x * SPRITE_SCALE * width
        self.center_y = center_y * SPRITE_SCALE * height

        self.textures = []
        self.textures.append(arcade.load_texture(
            "Sprites/coin.png",
            scale=SPRITE_SCALE))
        self.textures.append(arcade.load_texture(
            "Sprites/coin_01.png",
            scale=SPRITE_SCALE))
        # Make the animation start at a random point
        self.cur_texture_index = random.randrange(len(self.textures))
