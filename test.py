import arcade
import os
from Gui import GuiElement
from Player import Player
from Level import LevelGenerator

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

SPRITE_SCALE = 2
MOVEMENT_SPEED = 4
CAMERA_SPEED = 4
JUMP_SPEED = 13

GRAVITY = 0.5


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Init all attributes
        self.player = None
        self.player_engine = None
        self.sprite_list = None
        self.bloc_list = None
        self.background = None

        self.score_text = None

        self.score_nb_text = None

        self.is_game_over = False

    def setup(self):
        # Instanciate the sprite lists
        self.sprite_list = arcade.SpriteList()
        self.bloc_list = arcade.SpriteList()

        # Setup the player
        self.player = Player(120, 120)
        self.sprite_list.append(self.player)

        # Setup the GUI
        self.score_text = GuiElement(
            SCREEN_WIDTH - 80,
            SCREEN_HEIGHT - 20,
            40,
            40,
            "SCORE"
        )
        self.score_nb_text = GuiElement(
            SCREEN_WIDTH - 40,
            SCREEN_HEIGHT - 50,
            40,
            40,
            "100",
            align="right"
        )
        self.game_over_gui = GuiElement(
            SCREEN_WIDTH // 2 - 40,
            SCREEN_HEIGHT // 2,
            90,
            40,
            "Game over"
        )

        # Init Sounds
        # self.jump_sound = arcade.sound.load_sound("Sounds/jump.wav")
        self.die_sound = arcade.load_sound('Sounds/die.wav')

        # Load the background
        self.background = arcade.load_texture('Sprites/bg.png', scale=0.5)

        # Get the level bloc list
        self.generate_level()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.bloc_list,
            gravity_constant=GRAVITY
        )

        self.view_left = 0
        self.view_bottom = 0

    def on_key_press(self, key, modifiers):
        self.player.on_key_press(
            key,
            self.physics_engine.can_jump()
            # self.jump_sound
        )

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

        self.score_text.draw()
        self.score_nb_text.draw()

        if self.player.center_y < 0:
            if self.is_game_over is False:
                arcade.play_sound(self.die_sound)
                self.is_game_over = True

        if self.is_game_over:
            self.game_over_gui.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.player.center_y > 0:
            self.physics_engine.update()
            self.sprite_list.update()
            self.sprite_list.update_animation()
            if self.physics_engine.can_jump():
                self.player.update()

            changed = False
            if self.player.center_x > SCREEN_WIDTH // 2 + self.view_left:
                self.view_left += CAMERA_SPEED
                self.update_gui_position(self.view_left)
                changed = True

            if changed:
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)

    def generate_level(self):
        for i in range(15):
            bloc = arcade.Sprite('Sprites/bloc.png', SPRITE_SCALE)
            bloc.center_x = i * SPRITE_SCALE * 16
            bloc.center_y = 16
            self.bloc_list.append(bloc)

        bloc = arcade.Sprite('Sprites/bloc.png', SPRITE_SCALE)
        bloc.center_x = 16 * SPRITE_SCALE * 16
        bloc.center_y = 48
        self.bloc_list.append(bloc)
        bloc = arcade.Sprite('Sprites/bloc.png', SPRITE_SCALE)
        bloc.center_x = 16 * SPRITE_SCALE * 16
        bloc.center_y = 48 + 32
        self.bloc_list.append(bloc)

    def update_gui_position(self, offset=0):
        self.score_text.center_x += CAMERA_SPEED
        self.score_nb_text.center_x += CAMERA_SPEED
        self.game_over_gui.center_x += CAMERA_SPEED


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
