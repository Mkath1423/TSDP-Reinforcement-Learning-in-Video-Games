import pygame

from agent import Agent


class Player(Agent):
    def __init__(self, name, state):
        super().__init__(name, state)
    
    def get_move(self, game_state):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w]:
            return 0
        if keys[pygame.K_a]:
            return 1
        if keys[pygame.K_s]:
            return 2
        if keys[pygame.K_d]:
            return 3
        if self.state['cd'] <= 0:
            if keys[pygame.K_t]:
                return 5
            if keys[pygame.K_y]:
                return 6
            if keys[pygame.K_u]:
                return 7
            if keys[pygame.K_g]:
                return 8
            if keys[pygame.K_j]:
                return 9
            if keys[pygame.K_b]:
                return 10
            if keys[pygame.K_n]:
                return 11
            if keys[pygame.K_m]:
                return 12
            
        return 4