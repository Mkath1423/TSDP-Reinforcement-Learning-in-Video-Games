import enum

import pygame
import sys

from ai.ReplayMemory import State
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

    for agent_config in level_config.agents:
        level.add_agent(agent_type[agent_config.type](agent_config.name, agent_config.initial_state))

    ai_agents = {a.id: a for a in level.agents if isinstance(a, AIAgent)}

    last_state = level.get_state()

    while True:
        clock.tick(level_config.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")
        state = level.get_state()
        before_state = State(state["class_map"], None)

        agent_moves = level.get_moves(state)

        ai_moves = {k: v for k, v in agent_moves.items() if k in ai_agents.keys()}

        level.step_game(state, agent_moves)
        level.apply_collisions(state)

        done = level.is_over(state)

        level.update_states(state)
        after_state = State(state["class_map"], None)

        if last_state is not None:
            for a_id, a in ai_agents.items():
                if not ai_moves.__contains__(a_id):
                    continue
                a.remember(
                    before_state,
                    ai_moves[a_id],
                    a.get_reward(),
                    after_state,
                    done)

        if True:  # if do rendering
            level.render(screen)
            pygame.display.update()

        if True:  # if do training
            for a in ai_agents.values():
                a.train_short_memory()

                if True:  # some amount
                    a.train_long_memory()


if __name__ == "__main__":
    main()
