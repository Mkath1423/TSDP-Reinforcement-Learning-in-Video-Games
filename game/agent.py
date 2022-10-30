import abc
import pygame
import numpy as np


class Agent(pygame.sprite.Sprite, abc.ABC):

    def __init__(self, name, damage, health, position=(0, 0)):
        self.name = name
        self.damage = damage
        self.health = health
        self.position = np.asarray(position)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Agent({self.name}, {self.position})"

    @abc.abstractmethod
    def get_move(self, game_state):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
