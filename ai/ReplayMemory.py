from ai import log

import torch
import random

from collections import deque
from dataclasses import dataclass




@dataclass
class State:
    image: torch.tensor
    info: torch.tensor

    def __getitem__(self, item):
        return State(self.image[item], self.info[item])


@dataclass
class Transition:
    state: State
    action: int
    reward: int
    new_state: State
    is_done: bool


class ReplayMemory:

    def __init__(self, max_memory):
        self._memory = deque(maxlen=max_memory)

    def __len__(self):
        return len(self._memory)

    def append(self, transition):
        self._memory.append(transition)

    def get_last(self):
        sample = self._memory.pop()
        self._memory.append(sample)

        return sample

    def get_random_sample(self, size):
        return random.sample(self._memory, min(size, len(self)))

    def __getitem__(self, item):
        self._memory.__getitem__(item)
