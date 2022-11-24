import abc
import pygame
import numpy as np
import torch

from ai.ReplayMemory import ReplayMemory, Transition, State
from ai import model_config, trainer_config, log
from game.agent import Agent
from gameobject import GameObject
import pygame

from ai.model import PolicyNetwork, QTrainer
from utilities.files import save_yaml


class AIAgent(Agent):
    def __init__(self, name, state):
        self.model = PolicyNetwork(
            model_config.num_extra_inputs,
            model_config.num_outputs
        )

        self.trainer = QTrainer(
            self.model,
            trainer_config.lr,
            trainer_config.gamma,
            trainer_config.epsilon,
            4 + 8
        )

        self.replay_memory = ReplayMemory(10000)

        # gameobject class will set the name and id
        super().__init__(name, state)

    def get_reward(self):
        return self.get_state()["score"]

    def get_move(self, global_state):
        #save_yaml(global_state, r"tmp\global_state_example.yaml", default_flow_style=True)

        image = global_state["class_map"]
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

        transition = self.replay_memory.get_last()

        state: State = transition.state
        action = torch.tensor([transition.action], dtype=torch.long)
        reward = torch.tensor([transition.reward], dtype=torch.float)
        new_state: State = transition.new_state
        is_done = [transition.is_done]

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
