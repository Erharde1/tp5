import random
import arcade
from game_state import GameState
from attack_animation import AttackAnimation, AttackType

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"


class MyGame(arcade.Window):
    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        # Redimensionner les sprites
        self.player_sprite = arcade.Sprite("assets/player.png", scale=0.32, center_x=self.PLAYER_IMAGE_X,
                                           center_y=self.PLAYER_IMAGE_Y)
        self.computer_sprite = arcade.Sprite("assets/computer.png", scale=1.5, center_x=self.COMPUTER_IMAGE_X,
                                             center_y=self.COMPUTER_IMAGE_Y)

        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = None
        self.computer_attack_type = None
        self.player_attack_chosen = False
        self.game_state = GameState.NOT_STARTED
        self.attack_animation = None
        self.player_attack_sprite = None
        self.computer_attack_sprite = None

    def setup(self):
        self.player_score = 0
        self.computer_score = 0
        self.reset_round()

    def reset_round(self):
        self.player_attack_type = None
        self.computer_attack_type = None
        self.player_attack_chosen = False
        self.attack_animation = None
        self.player_attack_sprite = None
        self.computer_attack_sprite = None
        if self.player_score == 3 or self.computer_score == 3:
            self.game_state = GameState.GAME_OVER
        else:
            self.game_state = GameState.ROUND_ACTIVE

    def on_draw(self):
        arcade.start_render()
        self.draw_instructions()
        self.draw_scores()
        self.player_sprite.draw()
        self.computer_sprite.draw()
        if self.game_state == GameState.ROUND_ACTIVE and self.player_attack_chosen:
            if self.attack_animation:
                self.attack_animation.draw()
            if self.player_attack_sprite:
                self.player_attack_sprite.draw()
            if self.computer_attack_sprite:
                self.computer_attack_sprite.draw()
        elif self.game_state == GameState.ROUND_DONE:
            self.draw_results()

    def on_update(self, delta_time):
        if self.attack_animation:
            self.attack_animation.update(delta_time)
        if self.game_state == GameState.ROUND_ACTIVE and self.player_attack_chosen and not self.computer_attack_type:
            self.computer_attack_type = random.choice(list(AttackType))
            self.create_attack_sprites()
            self.validate_victory()

    def validate_victory(self):
        if self.player_attack_type == self.computer_attack_type:
            self.round_result = "Draw"
        elif (self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS) or \
                (self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK) or \
                (self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER):
            self.player_score += 1
            self.round_result = "Player wins"
        else:
            self.computer_score += 1
            self.round_result = "Computer wins"
        self.game_state = GameState.ROUND_DONE

    def create_attack_sprites(self):
        if self.player_attack_type:
            self.player_attack_sprite = AttackAnimation(self.player_attack_type)
            self.player_attack_sprite.center_x = self.PLAYER_IMAGE_X
            self.player_attack_sprite.center_y = self.PLAYER_IMAGE_Y - 80  # Ajuste pour afficher sous l'image du joueur

        if self.computer_attack_type:
            self.computer_attack_sprite = AttackAnimation(self.computer_attack_type)
            self.computer_attack_sprite.center_x = self.COMPUTER_IMAGE_X
            self.computer_attack_sprite.center_y = self.COMPUTER_IMAGE_Y - 80  # Ajuste pour afficher sous l'image du robot

    def draw_scores(self):
        arcade.draw_text(f"Player Score: {self.player_score}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Computer Score: {self.computer_score}", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 20,
                         arcade.color.WHITE, 14)

    def draw_instructions(self):
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Press SPACE to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 20,
                             anchor_x="center")
        elif self.game_state == GameState.GAME_OVER:
            arcade.draw_text("Game Over! Press SPACE to restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, 20, anchor_x="center")
        elif self.game_state == GameState.ROUND_ACTIVE and not self.player_attack_chosen:
            arcade.draw_text("Click to choose your attack: Rock (left), Paper (middle), Scissors (right)",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 14, anchor_x="center")

    def draw_results(self):
        result_text = f"Round Result: {self.round_result}"
        arcade.draw_text(result_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Press SPACE to continue", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, arcade.color.WHITE, 14,
                         anchor_x="center")

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED or self.game_state == GameState.GAME_OVER:
                self.setup()
            elif self.game_state == GameState.ROUND_DONE:
                self.reset_round()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.game_state == GameState.ROUND_ACTIVE and not self.player_attack_chosen:
            if x < SCREEN_WIDTH // 3:
                self.player_attack_type = AttackType.ROCK
            elif x < 2 * SCREEN_WIDTH // 3:
                self.player_attack_type = AttackType.PAPER
            else:
                self.player_attack_type = AttackType.SCISSORS

            self.player_attack_chosen = True
            self.attack_animation = AttackAnimation(self.player_attack_type)
            self.attack_animation.center_x = self.PLAYER_IMAGE_X
            self.attack_animation.center_y = self.PLAYER_IMAGE_Y - 80  # Ajuste pour afficher sous l'image du joueur


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
