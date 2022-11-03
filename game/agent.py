import abc
import pygame
import numpy as np

from gameobject import GameObject


class Agent(GameObject, abc.ABC):

    def __init__(self, name, damage, health, position=(0, 0)):
        
        self.damage = damage
        self.health = health
        self.position = np.asarray(position)

        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)
        
        # gameobject class will set the name and id
        super().__init__(name)

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
