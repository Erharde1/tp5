import random
import arcade
from game_state import GameState
from attack_animation import AttackAnimation, AttackType

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"


class MyGame(arcade.Window):
    # position des images du joueur et robot
    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 1.8
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 1.8

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.player_sprite = arcade.Sprite("assets/player.png", scale=0.4, center_x=self.PLAYER_IMAGE_X,
                                           center_y=self.PLAYER_IMAGE_Y)
        self.computer_sprite = arcade.Sprite("assets/computer.png", scale=1.7, center_x=self.COMPUTER_IMAGE_X,
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
        self.show_titles = True  # afficher les titres si true
        self.create_attack_options()
        self.computer_placeholder = arcade.SpriteSolidColor(100, 100, arcade.color.BLACK)
        self.computer_placeholder.center_x = self.COMPUTER_IMAGE_X
        self.computer_placeholder.center_y = self.COMPUTER_IMAGE_Y - 120

    def create_attack_options(self):
        # images d'attaque
        self.attack_options = {
            AttackType.ROCK: arcade.Sprite("assets/rock.png", scale=0.5),
            AttackType.PAPER: arcade.Sprite("assets/paper.png", scale=0.5),
            AttackType.SCISSORS: arcade.Sprite("assets/scissors.png", scale=0.5)
        }
        for i, (attack_type, sprite) in enumerate(self.attack_options.items()):
            sprite.center_x = self.PLAYER_IMAGE_X + (i - 1) * 110
            sprite.center_y = self.PLAYER_IMAGE_Y - 120

    def setup(self):
        self.player_score = 0
        self.computer_score = 0
        self.reset_round()

    def reset_round(self):
        # reset les variables pour une nouvelle partie
        self.player_attack_type = None
        self.computer_attack_type = None
        self.player_attack_chosen = False
        self.attack_animation = None
        self.player_attack_sprite = None
        self.computer_attack_sprite = None
        for sprite in self.attack_options.values():
            sprite.visible = True
        if self.player_score == 3 or self.computer_score == 3:
            self.game_state = GameState.GAME_OVER
        else:
            self.game_state = GameState.ROUND_ACTIVE

    def on_draw(self):
        arcade.start_render()
        # afficher instructions + score
        self.draw_instructions()
        self.draw_scores()
        # afficher les images du joueur et du robot
        self.player_sprite.draw()
        self.computer_sprite.draw()

        for sprite in self.attack_options.values():
            sprite.draw()
            arcade.draw_rectangle_outline(sprite.center_x, sprite.center_y, sprite.width, sprite.height,
                                          arcade.color.RED, 2)
        arcade.draw_rectangle_outline(self.computer_placeholder.center_x, self.computer_placeholder.center_y,
                                      self.computer_placeholder.width, self.computer_placeholder.height,
                                      arcade.color.RED, 2)
        if self.game_state in [GameState.ROUND_ACTIVE, GameState.ROUND_DONE]:
            if self.computer_attack_sprite:
                self.computer_attack_sprite.draw()
        if self.game_state == GameState.ROUND_DONE:
            self.draw_results()

    def on_update(self, delta_time):
        # changer les attaques
        if self.attack_animation:
            self.attack_animation.update(delta_time)
        if self.game_state == GameState.ROUND_ACTIVE and self.player_attack_chosen and not self.computer_attack_type:
            self.computer_attack_type = random.choice(list(AttackType))
            self.create_attack_sprites()
            self.validate_victory()

    def validate_victory(self):
        # trouver qui a gagne
        if self.player_attack_type == self.computer_attack_type:
            self.round_result = "Égalité"
        elif (self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS) or \
                (self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK) or \
                (self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER):
            self.player_score += 1
            self.round_result = "Le joueur a gagné!"
        else:
            self.computer_score += 1
            self.round_result = "L'ordinateur a gagné!"
        self.game_state = GameState.ROUND_DONE

    def create_attack_sprites(self):
        # images pour les attaqies
        if self.player_attack_type:
            self.player_attack_sprite = arcade.Sprite(f"assets/{self.player_attack_type.name.lower()}.png", scale=0.5)
            self.player_attack_sprite.center_x = self.PLAYER_IMAGE_X
            self.player_attack_sprite.center_y = self.PLAYER_IMAGE_Y - 80

        if self.computer_attack_type:
            self.computer_attack_sprite = arcade.Sprite(f"assets/{self.computer_attack_type.name.lower()}.png",
                                                        scale=0.5)
            self.computer_attack_sprite.center_x = self.COMPUTER_IMAGE_X
            self.computer_attack_sprite.center_y = self.COMPUTER_IMAGE_Y - 120

    def draw_scores(self):
        # afficher les scores du robot et du joueur
        arcade.draw_text(f"Le pointage du joueur est {self.player_score}", self.PLAYER_IMAGE_X, self.PLAYER_IMAGE_Y - 250,
                         arcade.color.WHITE, 14, anchor_x="center")
        arcade.draw_text(f"Le pointage de l'ordinateur est {self.computer_score}", self.COMPUTER_IMAGE_X, self.COMPUTER_IMAGE_Y - 250,
                         arcade.color.WHITE, 14, anchor_x="center")

    def draw_instructions(self):
        # afficher les instructions du jeu
        if self.show_titles:  # Seulement afficher les titres si true
            arcade.draw_text("Roche, papier, ciseaux", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, arcade.color.DARK_RED, 50,
                             anchor_x="center")
            arcade.draw_text("Appuyer sur une image pour faire une attaque!", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, arcade.color.BLUE, 20,
                             anchor_x="center")
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Appuyer sur ESPACE pour commencer", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 20,
                             anchor_x="center")
        elif self.game_state == GameState.GAME_OVER:
            arcade.draw_text("La partie est terminée! Appuyer sur ESPACE pour commencer une nouvelle partie", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.4,
                             arcade.color.WHITE, 20, anchor_x="center")

    def draw_results(self):
        # resultat des parties
        result_text = f"Résultat de la partie: {self.round_result}"
        arcade.draw_text(result_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, arcade.color.WHITE, 20,
                         anchor_x="center")
        arcade.draw_text("Appuyer sur ESPACE pour continuer", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, arcade.color.WHITE, 14,
                         anchor_x="center")

    def on_key_press(self, key, key_modifiers):
        # faire avancer la partie
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED or self.game_state == GameState.GAME_OVER:
                self.setup()
            elif self.game_state == GameState.ROUND_DONE:
                self.reset_round()

    def on_mouse_press(self, x, y, button, key_modifiers):
        # choisir les attaques
        if self.game_state == GameState.ROUND_ACTIVE and not self.player_attack_chosen:
            for attack_type, sprite in self.attack_options.items():
                if sprite.collides_with_point((x, y)):
                    self.player_attack_type = attack_type
                    self.player_attack_chosen = True
                    for other_sprite in self.attack_options.values():
                        if other_sprite != sprite:
                            other_sprite.visible = False
                    self.player_attack_sprite = arcade.Sprite(f"assets/{self.player_attack_type.name.lower()}.png",
                                                              scale=0.5)
                    self.player_attack_sprite.center_x = self.PLAYER_IMAGE_X
                    self.player_attack_sprite.center_y = self.PLAYER_IMAGE_Y - 80
                    break

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
