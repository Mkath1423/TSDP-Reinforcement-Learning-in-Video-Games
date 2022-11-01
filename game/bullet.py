import pygame
from gameobject import GameObject, GameObjectGroup
import agent


# haven't applied to the dictionary


class Bullets(GameObject):
    def __init__(self, player, player2, direction, d=3, velocity=3):
        pygame.sprite.Sprite.__init__(self)
        self.d = d
        self.image = pygame.Surface((d, d))
        self.position = player.position
        # need to determine the side and to make it more specific
        self.rect = self.image.get_rect(topleft=self.position)
        self.velocity = velocity
        self.damage = player.damage
        self.player2 = player2
        self.direction = direction
        bullets.append(self.position)

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.velocity
        elif self.direction == 'left':
            self.rect.x -= self.velocity
        elif self.direction == 'down':
            self.rect.y += self.velocity
        elif self.direction == 'right':
            self.rect.x += self.velocity
        else:  # if it needs angles
            pass

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
