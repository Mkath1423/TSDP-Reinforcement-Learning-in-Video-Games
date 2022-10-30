import pygame
import sys
from level import Level

pygame.init()
screen = pygame.display.set_mode((600, 1000))
clock = pygame.time.Clock()
level = Level()

level.add_agent("hi")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("black")
    level.render(screen)

    pygame.display.update()
    clock.tick(60)