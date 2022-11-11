from collections import deque
from dataclasses import dataclass
import random

@dataclass
class Transition:
    state: dict
    action: int
    reward: int
    new_state: dict
    is_done: bool


class ReplayMemory:

    def __init__(self, max_memory):
        self._memory = deque(maxlen=max_memory)

    def __len__(self):
        return len(self._memory)

    def append(self, transition):
        self._memory.append(transition)

    def get_random_sample(self, size):
        random.sample(self._memory, min(size, len(self)))
        