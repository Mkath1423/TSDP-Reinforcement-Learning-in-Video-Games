from game import log

import abc

import pygame

from game.gameobject import GameObject


class Agent(GameObject, abc.ABC):

    def __init__(self, name, state):

        # constant information
        self.initial_position = state.get("position", (0, 0))
        self.size = state.get("size", (50, 50))
        self.color = state.get("color", (0, 0, 255))
        self.max_hp = state.get("max_hp", 10)
        self.shoot_cooldown = state.get("shoot_cooldown", 60)
        self.movement_speed = state.get("movement_speed", 10)

        # variable state
        self.state = {
            "position": self.initial_position,
            "cd": self.shoot_cooldown,
            "hp": self.max_hp,
            "score": 0
        }

        # for pygame render
        self.image = pygame.Surface((self.size[0], self.size[1]))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.state["position"])

        # gameobject class will set the name and id
        super().__init__(name, state.get("class_label", 0))

    def reset(self):
        self.state = {
            "position": self.initial_position,
            "cd": self.shoot_cooldown,
            "hp": self.max_hp,
            "score": 0
        }

    def __repr__(self):
        return f"Agent({self.name}, {self.get_state()})"

    def get_state(self):
        return self.state

    def update_state(self, new_state):
        # update tracked state
        self.state = new_state

        # update dependencies of that state
        self.rect.x = self.state["position"][0]
        self.rect.y = self.state["position"][1]

    @abc.abstractmethod
    def get_move(self, game_state):
        pass
