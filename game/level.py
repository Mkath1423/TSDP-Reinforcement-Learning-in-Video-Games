import pygame
from gameobject import GameObject, GameObjectGroup
from agent import Agent
from bullet import Bullet

class Level():
    def __init__(self):
        self.agents_states = {}
        self.bullets_states = {}

        self.agents = GameObjectGroup("agents")
        self.bullets = GameObjectGroup("bullets")
        self.render_on = False

    def toggle_render(self, render_on):
        self.render_on = render_on

    def add_agent(self, name, damage, health, state, color=(255,0,0)):
        new_agent = Agent(name, damage, health, state, color)
        self.agents_states[new_agent.get_id] = state
        if self.render_on:
            self.agents.add(new_agent)

    def add_bullet(self, name, state):
        new_bullet = Bullet(name, state)
        self.bullets_states[new_bullet.get_id] = state
        if self.render_on:
            self.bullets.add(new_bullet)

    def update_states(self, new_agents_states):
        self.agents_states = new_agents_states

        for a in self.agents:
            a.update_state(new_agents_states[a.get_id])

        for b in self.bullets:
            pos = self.bullets_states[b.get_id]['position']
            v = self.bullets_states[b.get_id]['velocity']
            new_pos = (pos[0]+v[0], pos[1]+v[1])
            self.bullets_states[b.get_id]['position'] = new_pos
            b.update_state(self.bullets_states[b.get_id])

    def render(self, screen):
        assert(self.render_on)
        self.agents.update()
        self.agents.draw(screen)
        self.bullets.update()
        self.bullets.draw(screen)
