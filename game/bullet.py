import pygame

# haven't applied to the dictionary
class Bullets(pygame.sprite.Sprite):
    def __init__(self, agent_self, agent_others):
        super().__init__()
        self.image = pygame.image.load(images / red_dot.png)
        self.position = agent_self.position
        # need to determine the side and to make it more specific
        self.rect = self.image.get_rect(self.position)
        self.velocity = 3  # change later
        self.damage = agent_self.damage

    def change_state(self, damage):
        agent_others.health -= damage

    def update(self, new_state):
        pass

    def draw(self):
        pass
