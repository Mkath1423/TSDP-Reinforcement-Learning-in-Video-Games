import pygame
from gameobject import GameObject, GameObjectGroup
from agent import Agent

class Level():
    def __init__(self):
        self.states = {}
        self.game_objects = pygame.sprite.Group()
        self.render_on = True

    def add_object(self, obj):
        if self.render_on:
            self.game_objects.add(obj)

    def add_agent(self, name, position=(0,0)):
        if self.render_on:
            self.game_objects.add(Agent(name, position))

    def render(self, screen):
        assert(self.render_on)
        self.game_objects.update()
        self.game_objects.draw(screen)
