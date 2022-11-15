import abc
import pygame
import numpy as np
import torch

from ai.ReplayMemory import ReplayMemory, Transition, State
from game.agent import Agent
from gameobject import GameObject
import pygame

from ai.model import PolicyNetwork, QTrainer


class AIAgent(Agent):
    def __init__(self, name, damage, health, position=(0, 0)):
        self.model = PolicyNetwork(0, 5)

        self.trainer = QTrainer(self.model, 0.001, 0.8, 5)

        self.replay_memory = ReplayMemory(10000)

        # gameobject class will set the name and id
        super().__init__(name, damage, health, position=(0, 0))

    def update(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def get_move(self, global_state):
        image = None
        info = None

        return self.trainer.get_move(State(image, info))

    def remember(self,
                 previous_state,
                 action, reward,
                 new_state,
                 done):
        self.replay_memory.append(Transition(previous_state, action, reward, new_state, done))

    def train_short_memory(self):
        if len(self.replay_memory) == 0:
            return

        transition = self.replay_memory[-1]


        state: State = transition.state
        action: int = transition.action
        reward: int = transition.reward
        new_state: State = transition.new_state
        is_done: bool = transition.is_done

        self.trainer.train_step(state, action, reward, new_state, is_done)

    def train_long_memory(self):
        if len(self.replay_memory) == 0:
            return

        transitions = self.replay_memory.get_random_sample(1000)

        state: State = State(
                torch.stack([t.state.image for t in transitions]).to(dtype=torch.float),
                torch.stack([t.state.info for t in transitions]).to(dtype=torch.float)
            )
        action = torch.tensor([t.action for t in transitions]).to(dtype=torch.long)
        reward = torch.tensor([t.reward for t in transitions]).to(dtype=torch.float)

        new_state: State = State(
                torch.stack([t.new_state.image for t in transitions]).to(dtype=torch.float),
                torch.stack([t.new_state.info for t in transitions]).to(dtype=torch.float)
            )
        is_done = [t.is_done for t in transitions]

        self.trainer.train_step(state, action, reward, new_state, is_done)
