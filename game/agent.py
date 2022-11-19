import abc
import pygame
import numpy as np
from random import randint

from game import log
from gameobject import GameObject


class Agent(GameObject, abc.ABC):

    def __init__(self, name, state, color=(255,0,0)):
        
        self.state = state

        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = self.state["position"])
        
        # gameobject class will set the name and id
        super().__init__(name)

    def update(self):
        self.rect.x = self.state["position"][0]
        self.rect.y = self.state["position"][1]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Agent({self.name}, {self.state})"

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

    def get_move(self, game_state):
        log.debug(game_state)
        # TODO get predicted move
        i = randint(0,4)
        return i
