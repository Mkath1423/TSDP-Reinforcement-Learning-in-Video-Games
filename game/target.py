import random

from game import log

import pygame

from game.agent import Agent


class Target(Agent):
    def __init__(self, name, state):

        self.dont_move  = state.get("dont_move",  False)
        self.dont_shoot = state.get("dont_shoot", False)

        self.hold_move_duration = state.get("hold_move_duration", 20)
        self.hold_counter = 0

        self.last_choice = 0

        super().__init__(name, state)

    def get_move(self, game_state):
        self.hold_counter -= 1

        if not self.dont_shoot and self.state["cd"] < 0:
            return random.randint(5, 12)

        if not self.dont_move:
            if self.hold_counter <= 0:
                self.last_choice = random.randint(0, 4)
                self.hold_counter = self.hold_move_duration

            return self.last_choice

        return 0
