import arcade
import random
from Coin import Coin

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

SPRITE_SCALE = 2
MOVEMENT_SPEED = 8
CAMERA_SPEED = 8
JUMP_SPEED = 13

GRAVITY = 0.5


class LevelGenerator:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        f = open('background', 'r')
        for y, line in enumerate(self.reverse_lines(f)):
            line = self.split(line.rstrip('\n'))
            for x, value in enumerate(line):
                if value != '0':
                    # print(value)
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
        self.coin_list.update()
        self.coin_list.update_animation()
        for coin in arcade.check_for_collision_with_list(player, self.coin_list):
            print(coin)
            coin.kill()
            self.player.score += 200

    def split(self, str):
        return [str[start+1] for start in range(0, len(str) - 1, 1)]

    def reverse_lines(self, file):
        lines = []
        for line in reversed(file.readlines()):
            lines.append(line.rstrip('\n'))
        return lines
