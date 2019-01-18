import arcade
import random
from Coin import Coin
from Consts import SPRITE_SCALE


class LevelGenerator:
    def __init__(self):
        """Generate the level"""
        self.sprite_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.width = 0

        # Open the level
        f = open('Levels/1-1.lvl', 'r')

        # Create all blocs
        for y, line in enumerate(self.reverse_lines(f)):
            line = self.split(line.rstrip('\n'))
            for x, value in enumerate(line):
                self.width += 16 * SPRITE_SCALE
                if value != '0':
                    bloc = None
                    if value == '1':
                        bloc = arcade.Sprite(
                            'Sprites/bloc.png',
                            SPRITE_SCALE
                        )
                    elif value == '2':
                        bloc = arcade.Sprite(
                            'Sprites/Box.png',
                            SPRITE_SCALE
                        )
                    elif value == '3':   
                        bloc = arcade.Sprite(
                            'Sprites/mysterybox.png',
                            SPRITE_SCALE
                        )
                    elif value == '4':
                        bloc = arcade.Sprite(
                            'Sprites/pipe_tl.png',
                            SPRITE_SCALE
                        )
                    elif value == '5':
                        bloc = arcade.Sprite(
                            'Sprites/pipe_tr.png',
                            SPRITE_SCALE
                        )
                    elif value == '6':
                        bloc = arcade.Sprite(
                            'Sprites/pipe_dl.png',
                            SPRITE_SCALE
                        )
                    elif value == '7':
                        bloc = arcade.Sprite(
                            'Sprites/pipe_dr.png',
                            SPRITE_SCALE
                        )
                    elif value == '8':
                        # Creae a new coin
                        self.coin_list.append(Coin(x, y))
                        continue
                    # Set bloc base data
                    bloc.center_x = x * bloc.width
                    bloc.center_y = y * bloc.height
                    self.sprite_list.append(bloc)

    def draw(self):
        """Draw all lists"""
        self.sprite_list.draw()
        self.coin_list.draw()

    def update(self, player):
        """Update the level state"""
        self.score_change = 0
        self.coin_list.update()
        self.coin_list.update_animation()

        # Check collisions in all coins
        for coin in self.coin_list:
            if coin.left < player.right\
                and coin.right > player.left\
                and coin.top > player.bottom\
                and coin.bottom < player.top:
                arcade.play_sound(arcade.load_sound('Sounds/coin.wav'))
                coin.kill()
                self.score_change += 200

    def split(self, str):
        """Split the level string"""
        return [str[start+1] for start in range(0, len(str) - 1, 1)]

    def reverse_lines(self, file):
        """Reverse the file lines"""
        lines = []
        for line in reversed(file.readlines()):
            lines.append(line.rstrip('\n'))
        return lines
