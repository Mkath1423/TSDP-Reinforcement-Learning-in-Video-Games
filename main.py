import itertools
import os
import sys
import time
import random

import numpy as np
import torch
import pygame

from ai.ReplayMemory import State
from ai import log

from game import level_config
from game.AI_Agent import AIAgent
from game.player import Player
from game.level import Level

from ai import model_config, trainer_config
from game.target import Target
from utilities import get_config
from utilities.checkpoints import save_checkpoint

class_map = {
    "teammate": 4,
    "enemy": 3,
    "bullet": 2,
    "obstacle": 1,
}

agent_type = {
    "AIAgent": AIAgent,
    "Target": Target,
    "Player": Player
}


def main():
    pygame.init()

    width = level_config.window_size[0]
    height = level_config.window_size[1]

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(level_config.title)

    all_agents = []
    for agent_config in level_config.agents:
        all_agents.append(agent_type[agent_config.type](agent_config.name, agent_config.initial_state))

    ai_id, ai_agent = [(a.id, a) for a in all_agents if isinstance(a, AIAgent)][0]

    for epoch in range(200):

        level = Level()
        last_state = level.get_state()

        for a in all_agents:
            a.reset()
            level.add_agent(a)

        score_per_iteration = []
        time_per_iteration = []

        for iteration in itertools.count():
            iteration_start_time = time.process_time()  # for logging
            # poll events for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill("black")
            state = level.get_state()
            before_state = State(state["class_map"],
                                 torch.tensor([[1 if ai_agent.get_cd() < 0 else -1]], dtype=torch.float32))

            agent_moves = level.get_moves(state)

            if agent_moves.__contains__(ai_id):
                ai_move = agent_moves[ai_id]

                level.step_game(state, agent_moves)
                level.apply_collisions(state)

                done = level.is_over(state) or iteration > 300
                reward = ai_agent.get_reward() - (iteration * 0.05) - (20 if ai_agent.get_hp() <= 0 else 0)

                level.update_states(state)
                after_state = State(state["class_map"],
                                    torch.tensor(torch.tensor([[1 if ai_agent.get_cd() < 0 else -1]], dtype=torch.float32)))

                if last_state is not None:
                    ai_agent.remember(
                        before_state,
                        ai_move,
                        reward,
                        after_state,
                        done)
            else:
                done = True

            if True:  # if do rendering
                level.render(screen)
                pygame.display.update()

            if not trainer_config.eval:  # if do training
                ai_agent.train_short_memory()

                if iteration % 100 == 0 and False:  # some amount
                    ai_agent.train_long_memory()

            iteration_time = time.process_time() -  iteration_start_time

            if iteration % 1 == 0:
                log.info(f"[{epoch}, {iteration}] batch_runtime: {iteration_time:0.4f} scores: {reward} move: {ai_move}")

            score_per_iteration.append(reward)
            time_per_iteration.append(iteration_time)

            if done:
                ai_agent.trainer.epsilon *= 0.95

                log.info(f"Completed Epoch : {epoch}/100 avg_batch_runtime: {np.average(time_per_iteration):0.4f}"
                         f" avg_scores: {np.average(score_per_iteration):0.4f}"
                         )

                if (epoch + 1) % 20 == 0:
                    path = os.path.join("checkpoints", f"multi_direction_{np.average(score_per_iteration):0.3f}_ep_{epoch}.pt")
                    save_checkpoint(path, ai_agent.model, ai_agent.trainer.optimizer, config=get_config())

                break





if __name__ == "__main__":
    main()
