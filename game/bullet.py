import pygame
import abc

from gameobject import GameObject, GameObjectGroup


# haven't applied to the dictionary


class Bullet(GameObject, abc.ABC):
    def __init__(self, name, state):
        pygame.sprite.Sprite.__init__(self)
        self.state = state

        # need to determine the side and to make it more specific
        self.image = pygame.Surface((5, 5))
        self.image.fill("yellow")
        self.rect = self.image.get_rect(topleft=self.state['position'])

        super().__init__(name)

    def update(self):
        self.rect.x = self.state['position'][0]
        self.rect.y = self.state['position'][1]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Bullet({self.name}, {self.state['position']}, {self.state['velocity']})"

    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

    def update_state(self, new_state):
        self.state = new_state

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