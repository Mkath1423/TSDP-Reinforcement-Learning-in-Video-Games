import pygame
import sys
from level import Level
from bullet import Bullets
import agent

pygame.init()
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arena")
clock = pygame.time.Clock()
level = Level()

level.add_agent("hi")


def main():
    clock = pygame.time.Clock()
    cont = True

    bullets = []

    while cont:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cont = False
                pygame.quit()
                sys.exit()
        screen.fill("black")
        level.render(screen)

        for bullet in bullets:
            Bullets.draw(bullet)
        pygame.display.update()

    main()


if __name__ == "__main__":
    main()
