import time

import numpy as np
import pygame
import torch

from gameobject import GameObject, GameObjectGroup
from agent import Agent
from bullet import Bullet
from player import Player
import numpy
from matplotlib import pyplot as plt

from game import log, level_config

move_set = ['w', 'a', 's', 'd', 'rest']

v_by_dir = [
    (-4, -4), (0, -5), (4, -4),
    (-5, 0), (5, 0),
    (-4, 4), (0, 5), (4, 4)
]

class Level:
    def __init__(self):
        self.agents = GameObjectGroup("agents")
        self.bullets = GameObjectGroup("bullets")

    def add_agent(self, agent: Agent):
        self.agents.add(agent)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def get_state(self):
        agent_states = self.agents.get_state()
        bullet_states = self.bullets.get_state()

        surface = np.zeros((level_config.window_size[0], level_config.window_size[1]))
        self.agents.render_class_map(surface)
        self.bullets.render_class_map(surface)

        cur_states = {
            "agents": agent_states,
            "bullets": bullet_states,
            "class_map": torch.from_numpy(surface).to(dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        }

        return cur_states

    def update_states(self, state):
        self.agents.update_state(state["agents"])
        self.bullets.update_state(state["bullets"])

    def get_moves(self, state):
        return self.agents.get_moves(state)

    def step_game(self, state, agent_moves):
        agent_states = state["agents"]
        bullet_states = state["bullets"]

        for i in agent_states:
            x, y = agent_states[i]['position']
            if 5 <= agent_moves[i] <= 12:
                agent_center = (x + 25, y + 25)
                v = v_by_dir[agent_moves[i] - 5]

                bullet_config = level_config.bullet.initial_state.copy()
                bullet_config.update({'position': agent_center, 'velocity': v, 'source': i})

                self.add_bullet(
                    Bullet(bullet_config)
                )

                agent_states[i]['cd'] = 60
                continue

            move = move_set[agent_moves[i]]
            if move == 'w':
                y -= 5
            elif move == 'a':
                x -= 5
            elif move == 's':
                y += 5
            elif move == 'd':
                x += 5
            elif move == 'rest':
                pass

            if x < 0:  # prevents the agents from going out of the screen
                x = 0
            elif x > 950:
                x = 950
            if y < 0:
                y = 0
            elif y > 750:
                y = 750

            agent_states[i]['position'] = (x, y)
            if agent_states[i]['cd'] <= 0:
                continue
            agent_states[i]['cd'] -= 1

        for i in bullet_states:
            x, y = bullet_states[i]['position']
            v_x, v_y = bullet_states[i]['velocity']
            x += v_x
            y += v_y
            if x < 0 or x > 1000 or y < 0 or y > 800:  # delete if out of the screen
                bullet_states[i] = None
                continue
            bullet_states[i]['position'] = (x, y)

    def apply_collisions(self, state):
        agent_states = state["agents"]
        bullet_states = state["bullets"]

        for a in agent_states:
            if agent_states[a] is None:
                continue
            a_pos = agent_states[a]['position']

            for b in bullet_states:
                if bullet_states[b] is None:
                    continue
                b_pos = bullet_states[b]['position']

                source = bullet_states[b]['source']
                # on collision
                if (a_pos[0] < b_pos[0] + 5 and a_pos[0] + 50 > b_pos[0] and
                        a_pos[1] < b_pos[1] + 5 and a_pos[1] + 50 > b_pos[1]):
                    if source == a: continue  # bullet comes from the agent itself, skip

                    # agent on collision
                    agent_states[a]['hp'] -= 10

                    # give score for hitting opponent
                    if agent_states.__contains__(source):
                        agent_states[source]["score"] += 10

                    if agent_states[a]['hp'] <= 0:
                        agent_states[a] = None

                    # bullet on collision
                    bullet_states[b] = None

    def is_over(self, state):
        return len(state["agents"]) == 1

    def render(self, screen):
        self.agents.draw(screen)
        self.bullets.draw(screen)

    def __repr__(self):
        return f'agents:{self.agents}, bullets:{self.bullets}'
