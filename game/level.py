import pygame
from gameobject import GameObject, GameObjectGroup
from agent import Agent
from bullet import Bullet

class Level():
    def __init__(self):
        self.states = {}
        self.game_objects = pygame.sprite.Group()
        self.render_on = False

    def toggle_render(self, render_on):
        self.render_on = render_on

    def add_object(self, obj):
        if self.render_on:
            self.game_objects.add(obj)

    def add_agent(self, name, damage, health, position=(0,0)):
        if self.render_on:
            self.game_objects.add(Agent(name, damage, health, position))
            self.add_object(Agent(name, damage, health, position))

    def add_bullet(self, name, position=(0,0), velocity=(0,0)):
        if self.render_on:
            self.add_object(Bullet(name, position, velocity))

    def render(self, screen):
        assert(self.render_on)
        self.game_objects.update()
        self.game_objects.draw(screen)
