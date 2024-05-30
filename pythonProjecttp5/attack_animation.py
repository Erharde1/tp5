from enum import Enum
import arcade

class AttackType(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class AttackAnimation(arcade.Sprite):
    ATTACK_SCALE = 0.50
    ANIMATION_SPEED = 5.0

    def __init__(self, attack_type):
        super().__init__()

        self.attack_type = attack_type
        if self.attack_type == AttackType.ROCK:
            self.textures = [
                arcade.load_texture("assets/attack_rock.png"),
                arcade.load_texture("assets/rock.png"),
            ]
        elif self.attack_type == AttackType.PAPER:
            self.textures = [
                arcade.load_texture("assets/attack_paper.png"),
                arcade.load_texture("assets/paper.png"),
            ]
        else:
            self.textures = [
                arcade.load_texture("assets/attack_scissors.png"),
                arcade.load_texture("assets/scissors.png"),
            ]

        self.scale = self.ATTACK_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)
        self.animation_update_time = 1.0 / AttackAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0

    def update(self, delta_time):
        self.time_since_last_swap += delta_time
        if self.time_since_last_swap > self.animation_update_time:
            self.current_texture = (self.current_texture + 1) % len(self.textures)
            self.set_texture(self.current_texture)
            self.time_since_last_swap = 0.0
