import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CHARACTER_SCALE = 3
MOVEMENT_SPEED = 5
JUMP_SPEED = 10

GRAVITY = 0.5


# class Player(arcade.Sprite):
#     def __init__(self, right_textures, left_textures, jump_textures):
#         super().__init__("Sprites/mario_idle.png")
#         self.direction = 'none'

#         self.current_texture = 0
#         self.right_textures = right_textures
#         self.left_textures = left_textures
#         self.jump_textures = jump_textures

#     def update(self):
#         self.current_texture += 1

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Create the sprite lists
        self.sprite_list = arcade.SpriteList()
        self.bloc_list = arcade.SpriteList()

        # Set up the player
        # Character image from kenney.nl
        self.player = arcade.AnimatedWalkingSprite()
        self.player.stand_right_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=CHARACTER_SCALE)]
        self.player.stand_left_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=CHARACTER_SCALE, mirrored=True)]
        self.player.walk_right_textures = self.initWalk()
        self.player.walk_left_textures = self.initWalk(is_mirrored=True)

        self.player.texture_change_distance = 30
        self.player.center_x = 50  # Starting position
        self.player.center_y = 120
        self.sprite_list.append(self.player)

        for i in range(15):
            bloc = arcade.Sprite('Sprites/bloc.png', CHARACTER_SCALE)
            bloc.center_x = i * CHARACTER_SCALE * 16
            bloc.center_y = 16
            self.bloc_list.append(bloc)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                     self.bloc_list,
                                                     gravity_constant=GRAVITY)

    def initWalk(self, is_mirrored=False):
        anim = []
        anim.append(arcade.load_texture(
            "Sprites/mario_idle.png",
            scale=CHARACTER_SCALE,
            mirrored=is_mirrored))
        anim.append(arcade.load_texture(
            "Sprites/mario_walk1.png",
            scale=CHARACTER_SCALE,
            mirrored=is_mirrored))
        anim.append(arcade.load_texture(
            "Sprites/mario_walk2.png",
            scale=CHARACTER_SCALE,
            mirrored=is_mirrored))
        return anim

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.physics_engine.can_jump():
            self.player.stand_right_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=CHARACTER_SCALE)]
            self.player.stand_left_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=CHARACTER_SCALE, mirrored=True)]
            self.player.walk_right_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=CHARACTER_SCALE)]
            self.player.walk_left_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=CHARACTER_SCALE, mirrored=True)]
            self.player.change_y = JUMP_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x += MOVEMENT_SPEED
        if key == arcade.key.LEFT:
            self.player.change_x -= MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if self.physics_engine.can_jump():
            self.player.stand_right_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=CHARACTER_SCALE)]
            self.player.stand_left_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=CHARACTER_SCALE, mirrored=True)]
            self.player.walk_right_textures = self.initWalk()
            self.player.walk_left_textures = self.initWalk(is_mirrored=True)
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.sprite_list.draw()
        self.bloc_list.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.sprite_list.update()
        self.sprite_list.update_animation()

        self.physics_engine.update()
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
