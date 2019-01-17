import arcade
import os

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

SPRITE_SCALE = 2
MOVEMENT_SPEED = 4
CAMERA_SPEED = 2
JUMP_SPEED = 10

GRAVITY = 0.5


class Player(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()
        self.stand_right_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=SPRITE_SCALE)]
        self.stand_left_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=SPRITE_SCALE, mirrored=True)]
        self.walk_right_textures = self.initWalk()
        self.walk_left_textures = self.initWalk(is_mirrored=True)

        self.texture_change_distance = 30
        self.center_x = 50  # Starting position
        self.center_y = 120

    def initWalk(self, is_mirrored=False):
        anim = []
        anim.append(arcade.load_texture(
            "Sprites/mario_idle.png",
            scale=SPRITE_SCALE,
            mirrored=is_mirrored))
        anim.append(arcade.load_texture(
            "Sprites/mario_walk1.png",
            scale=SPRITE_SCALE,
            mirrored=is_mirrored))
        anim.append(arcade.load_texture(
            "Sprites/mario_walk2.png",
            scale=SPRITE_SCALE,
            mirrored=is_mirrored))
        return anim

    def update(self):
        self.stand_right_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=SPRITE_SCALE)]
        self.stand_left_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=SPRITE_SCALE, mirrored=True)]
        self.walk_right_textures = self.initWalk()
        self.walk_left_textures = self.initWalk(is_mirrored=True)

    def on_key_press(self, key, can_jump):
        if key == arcade.key.SPACE and can_jump:
            # [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE)]
            self.stand_right_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE)]
            self.stand_left_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE, mirrored=True)]
            self.walk_right_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE)]
            self.walk_left_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE, mirrored=True)]
            self.change_y = JUMP_SPEED
        elif key == arcade.key.RIGHT:
            self.change_x += MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.change_x -= MOVEMENT_SPEED

    def on_key_release(self, key):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.background = None

    def setup(self):
        # Create the sprite lists
        self.sprite_list = arcade.SpriteList()
        self.bloc_list = arcade.SpriteList()

        # Set up the player
        # Character image from kenney.nl
        self.player = Player()
        self.sprite_list.append(self.player)

        self.background = arcade.load_texture('Sprites/bg.png', scale=0.5)

        self.generate_level()

        bloc = arcade.Sprite('Sprites/bloc.png', SPRITE_SCALE)
        bloc.center_x = 16 * SPRITE_SCALE * 16
        bloc.center_y = 48
        self.bloc_list.append(bloc)
        bloc = arcade.Sprite('Sprites/bloc.png', SPRITE_SCALE)
        bloc.center_x = 16 * SPRITE_SCALE * 16
        bloc.center_y = 48 + 32
        self.bloc_list.append(bloc)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                        self.bloc_list,
                                                        gravity_constant=GRAVITY)

        self.view_left = 0
        self.view_bottom = 0

    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, self.physics_engine.can_jump())

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH//2 - 32,
            SCREEN_HEIGHT//2 + (32),
            (32 * 75) * 3,
            SCREEN_HEIGHT,
            self.background,
            repeat_count_x=3
        )
        self.sprite_list.draw()
        self.bloc_list.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.player.center_y < 0:
            print('game_over')
        else:
            self.physics_engine.update()
            self.sprite_list.update()
            self.sprite_list.update_animation()
            if self.physics_engine.can_jump():
                self.player.update()

            # changed = False
            # # Scroll right
            # right_bndry = self.view_left + SCREEN_WIDTH
            # if self.player.right > right_bndry // 2:
            self.view_left += CAMERA_SPEED
            #     changed = True

            # if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def generate_level(self):
        for i in range(75):
            bloc = arcade.Sprite('Sprites/bloc.png', SPRITE_SCALE)
            bloc.center_x = i * SPRITE_SCALE * 16
            bloc.center_y = 16
            self.bloc_list.append(bloc)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
