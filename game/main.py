import enum

import pygame
import sys

from game import log, level_config
from game.AI_Agent import AIAgent
from game.player import Player
from level import Level
import ai

class_map = {
    "teammate": 4,
    "enemy": 3,
    "bullet": 2,
    "obstacle": 1,
}

agent_type = {
    "AIAgent": AIAgent,
    "Target": Player,
    "Player": Player
}


def main():
    pygame.init()

    width = level_config.window_size[0]
    height = level_config.window_size[1]

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(level_config.title)
    clock = pygame.time.Clock()

    level = Level()
    level.toggle_render(True)

    for agent_config in level_config.agents:
        level.add_agent(agent_type[agent_config.type](agent_config.name, agent_config.initial_state))

    while True:
        clock.tick(level_config.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")

        level.update_states()
        level.collision()
        level.render(screen)


        pygame.display.update()


if __name__ == "__main__":
    main()
