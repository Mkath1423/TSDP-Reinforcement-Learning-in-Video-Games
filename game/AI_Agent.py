from game import log

import pygame

import torch

from ai import model_config, trainer_config, device
from ai.ReplayMemory import ReplayMemory, Transition, State
from ai.model import PolicyNetwork, QTrainer

from game.agent import Agent
from utilities.checkpoints import load_checkpoint


class AIAgent(Agent):
    def __init__(self, name, state):
        self.model = PolicyNetwork(
            model_config.num_extra_inputs,
            model_config.num_outputs
        )

        self.model.to(device=device)

        if model_config.checkpoint:
            valid, model, _, _ = load_checkpoint(model_config.checkpoint)

            if valid:
                self.model.load_state_dict(model)

        if trainer_config.eval:
            self.model.eval()

        self.trainer = QTrainer(
            self.model,
            trainer_config.lr,
            trainer_config.gamma,
            trainer_config.epsilon,
            model_config.num_outputs
        )

        self.replay_memory = ReplayMemory(10000)

        # gameobject class will set the name and id
        super().__init__(name, state)

    def get_reward(self):
        return self.get_state()["score"]

    def get_cd(self):
        return self.get_state()["cd"]

    def get_hp(self):
        return self.get_state()["hp"]

    def get_move(self, global_state):
        #save_yaml(global_state, r"tmp\global_state_example.yaml", default_flow_style=True)

        image = global_state["class_map"].to(device=device)
        info = torch.tensor([[1 if self.get_cd() < 0 else -1]], dtype=torch.float, device=device)

        return self.trainer.get_move(State(image, info))

    def train(self, is_train):
        if is_train:
            self.model.train()

        else:
            self.model.eval()

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

        state: State = State(
            transition.state.image.to(device=device),
            transition.state.info.to(device=device)
        )

        action = torch.tensor([transition.action], dtype=torch.long, device=device)
        reward = torch.tensor([transition.reward], dtype=torch.float, device=device)

        new_state: State = State(
            transition.new_state.image.to(device=device),
            transition.new_state.info.to(device=device)
        )

        is_done = torch.tensor([transition.is_done], dtype=torch.bool, device=device)

        # log.debug(
        #     f"state {state.image.shape} {state.info.shape}\n" +
        #     f"action {action.shape}\n" +
        #     f"reward {reward.shape}\n" +
        #     f"new state {new_state.image.shape} {new_state.info.shape}\n" +
        #     f"is done {is_done.shape}\n"
        # )

        self.trainer.train_step(state, action, reward, new_state, is_done)

    def train_long_memory(self):
        if len(self.replay_memory) == 0:
            return

        transitions = self.replay_memory.get_random_sample(500)

        state: State = State(
            torch.cat([t.state.image for t in transitions]).to(dtype=torch.float, device=device),
            torch.cat([t.state.info for t in transitions]).to(dtype=torch.float, device=device)
        )

        action = torch.tensor([t.action for t in transitions]).to(dtype=torch.long, device=device)
        reward = torch.tensor([t.reward for t in transitions]).to(dtype=torch.float, device=device)

        new_state: State = State(
            torch.cat([t.new_state.image for t in transitions]).to(dtype=torch.float, device=device),
            torch.cat([t.new_state.info for t in transitions]).to(dtype=torch.float, device=device)
        )

        is_done = torch.tensor([t.is_done for t in transitions], dtype=torch.bool, device=device)

        # log.debug(
        #     f"state {state.image.shape} {state.info.shape}\n" +
        #     f"action {action.shape}\n" +
        #     f"reward {reward.shape}\n" +
        #     f"new state {new_state.image.shape} {new_state.info.shape}\n" +
        #     f"is done {is_done.shape}\n"
        # )

        self.trainer.train_step(state, action, reward, new_state, is_done)
