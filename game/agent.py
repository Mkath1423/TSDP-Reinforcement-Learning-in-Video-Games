import abc

import numpy as np

from gameobject import GameObject
import pygame


class Agent(GameObject, abc.ABC):

    def __init__(self, name, position=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.position = np.asarray(position)

        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)

    def update(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Agent({self.name}, {self.position})"

    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    def get_state(self):
        pass

    def update_state(self, new_state):
        pass


    """ 
    @abc.abstractmethod
    def get_move(self, game_state):
        pass
    """

    """ sprite group should handle draw by itself
    @abc.abstractmethod
    def draw(self):
        pass
    """
