from game import log

import pygame

from game.gameobject import GameObject


class Bullet(GameObject):
    def __init__(self, state):
        pygame.sprite.Sprite.__init__(self)
        # constant information
        self.damage = state.get("damage", 1)
        self.speed = state.get("speed", 30)
        self.size = state.get("size", (5, 5))
        self.class_label = state.get("class_label", 2)

        # variable state
        self.state = {
            "position": state.get("position", (0, 0)),
            "velocity": (self.speed * state.get("velocity", (0, 0))[0],
                         self.speed * state.get("velocity", (0, 0))[1]),
            "source": state.get("source", -1),
        }

        # for pygame render
        self.image = pygame.Surface(self.size)
        self.image.fill("yellow")
        self.rect = self.image.get_rect(topleft=self.state['position'])

        super().__init__("bullet", self.class_label)

    def __repr__(self):
        return f"Bullet({self.name}, {self.state['position']}, {self.state['velocity']})"

    def get_state(self):
        return self.state

    def update_state(self, new_state):
        self.state = new_state

        self.rect.x = self.state['position'][0]
        self.rect.y = self.state['position'][1]

    def get_move(self, game_state):
        return 0

"""
    # substitution for pygame collide
    def collide(self):
        if (player2.rect.x - d) <= bullet.rect.x <= (player2.rect.x + 50):
            if (player2.rect.y - d) <= bullet.rect.y <= (player2.rect.y + 50):
                return True

    def bullet_damage(self):
        player2.health -= self.damage

    def change_state(self):
        if collide():
            bullet_damage()
            self.kill()

    def draw(self, bullet):
        pygame.draw.rect(screen, (255, 0, 0), bullet)
"""