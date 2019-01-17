import arcade
import random
from Coin import Coin
from Consts import SPRITE_SCALE


class LevelGenerator:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.width = 0

        f = open('Levels/1-1.lvl', 'r')
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
                        self.coin_list.append(Coin(x, y))
                        continue
                    bloc.center_x = x * bloc.width
                    bloc.center_y = y * bloc.height
                    self.sprite_list.append(bloc)

    def draw(self):
        self.sprite_list.draw()
        self.coin_list.draw()

    def update(self, player):
        self.score_change = 0
        self.coin_list.update()
        self.coin_list.update_animation()

        for coin in self.coin_list:
            if coin.left < player.right\
                and coin.right > player.left\
                and coin.top > player.bottom\
                and coin.bottom < player.top:
                arcade.play_sound(arcade.load_sound('Sounds/coin.wav'))
                coin.kill()
                self.score_change += 200

    def split(self, str):
        return [str[start+1] for start in range(0, len(str) - 1, 1)]

    def reverse_lines(self, file):
        lines = []
        for line in reversed(file.readlines()):
            lines.append(line.rstrip('\n'))
        return lines
