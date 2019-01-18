import arcade
from Consts import SPRITE_SCALE, MOVEMENT_SPEED, JUMP_SPEED


class Player(arcade.AnimatedWalkingSprite):
    """Player class"""
    def __init__(self, center_x, center_y):
        """Init animations and base parameters of the sprite"""
        super().__init__()

        # Init score
        self.score = 0

        # Init animations
        self.stand_right_textures = [arcade.load_texture(
            "Sprites/mario_idle.png",
            scale=SPRITE_SCALE)]
        self.stand_left_textures = [arcade.load_texture(
            "Sprites/mario_idle.png",
            scale=SPRITE_SCALE,
            mirrored=True)]
        self.walk_right_textures = self.initWalk()
        self.walk_left_textures = self.initWalk(is_mirrored=True)

        # Init base animation lag
        self.texture_change_distance = 30

        # Init starting position
        self.center_x = center_x
        self.center_y = center_y

    def initWalk(self, is_mirrored=False):
        """Init the walking animation (mirrored or not)"""
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
        """When the player needs to be updated"""
        # if len(self.walk_right_textures) == 1 and len(self.walk_left_textures) == 1:
        #     self.stand_right_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=SPRITE_SCALE)]
        #     self.stand_left_textures = [arcade.load_texture("Sprites/mario_idle.png", scale=SPRITE_SCALE, mirrored=True)]
        #     self.walk_right_textures = self.initWalk()
        #     self.walk_left_textures = self.initWalk(is_mirrored=True)
        pass

    def on_key_press(self, key, can_jump):
        """Handle all """
        if key == arcade.key.SPACE and can_jump:
            arcade.sound.play_sound(arcade.sound.load_sound("Sounds/jump.wav"))
            # self.stand_right_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE)]
            # self.stand_left_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE, mirrored=True)]
            # self.walk_right_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE)]
            # self.walk_left_textures = [arcade.load_texture("Sprites/mario_jump.png", scale=SPRITE_SCALE, mirrored=True)]
            self.change_y = JUMP_SPEED
        elif key == arcade.key.RIGHT:
            self.change_x += MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.change_x -= MOVEMENT_SPEED

    def on_key_release(self, key):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0
