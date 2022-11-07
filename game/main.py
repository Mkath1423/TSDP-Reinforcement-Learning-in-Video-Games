import pygame
import sys
from level import Level

def main():
    pygame.init()
    width = 1000
    height = 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Arena")
    clock = pygame.time.Clock()
    level = Level()
    level.toggle_render(True)
    level.add_agent("player1", 10, 10, state={'position':(180,350)})
    level.add_agent("player2", 10, 10, state={'position':(780, 350)}, color=(0,0,255))
    level.add_bullet('bullet 1', state={'position':(180, 350), 'velocity':(1,0)})
    level.add_bullet('bullet 2', state={'position':(180, 350), 'velocity':(2,1)})


    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")
        level.update_states(level.agents_states)
        level.render(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
