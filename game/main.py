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
    level.add_agent("test agent 1", 10, 10)
    level.add_bullet("test bullet 1")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")
        level.render(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
