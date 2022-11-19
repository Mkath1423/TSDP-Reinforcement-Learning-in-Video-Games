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

    level.add_agent("agent", state={'position':(180,350), 'hp':10, 'cd':60})
    level.add_agent("agent", state={'position':(780, 350), 'hp':10, 'cd':60}, color=(0,0,255))
    level.add_player("player", state={'position':(0, 0), 'hp':10, 'cd':60})


    while True:
        clock.tick(60)
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
