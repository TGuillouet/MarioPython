import arcade
import os
from Gui import GuiElement
from Player import Player
from Level import LevelGenerator
from Consts import *


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        # Redefine the main directory
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
        """Setup initial values"""
        # Instanciate the sprite lists
        self.sprite_list = arcade.SpriteList()

        # Setup the player
        self.player = Player(120, 120)
        self.sprite_list.append(self.player)

        # Setup the GUI
        self.score_text = GuiElement(
            80,
            SCREEN_HEIGHT - 20,
            40,
            40,
            "MARIO"
        )
        self.score_nb_text = GuiElement(
            80,
            SCREEN_HEIGHT - 50,
            40,
            40,
            "0" * 6,
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
        self.die_sound = arcade.load_sound('Sounds/die.wav')

        # Load the background
        self.background = arcade.load_texture('Sprites/bg.png', scale=0.5)

        # Get the level bloc list\
        self.level = LevelGenerator()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.level.sprite_list,
            gravity_constant=GRAVITY
        )

        self.view_left = 0

    def on_key_press(self, key, modifiers):
        """Handle the key press"""
        self.player.on_key_press(
            key,
            self.physics_engine.can_jump()
        )

    def on_key_release(self, key, modifiers):
        """Handle the key release"""
        self.player.on_key_release(key)

    def on_draw(self):
        """ Render the screen (draw all elements) """
        arcade.start_render()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH//2 - 48,
            SCREEN_HEIGHT//2 + 48,
            self.level.width,
            SCREEN_HEIGHT,
            self.background,
            repeat_count_x=50
        )
        self.sprite_list.draw()
        self.level.draw()

        self.score_text.draw()
        self.score_nb_text.draw_new_text(str(self.player.score).zfill(6))

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
            self.level.update(self.player)

            if self.physics_engine.can_jump():
                self.player.update()

            # Update the score of the player
            self.player.score += self.level.score_change

            #  Update the camera
            if self.player.center_x > SCREEN_WIDTH // 2 + self.view_left:
                self.view_left += CAMERA_SPEED
                self.update_gui_position(self.view_left)
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    0,
                                    SCREEN_HEIGHT)

    def update_gui_position(self, offset=0):
        """Update the position of the GUI when the camera moves"""
        self.score_text.center_x += CAMERA_SPEED
        self.score_nb_text.center_x += CAMERA_SPEED
        self.game_over_gui.center_x += CAMERA_SPEED


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
