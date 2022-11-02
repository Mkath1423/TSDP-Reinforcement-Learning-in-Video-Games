import pygame
import bullet
import agent

width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arena")

def main():
    clock = pygame.time.Clock()
    cont = True
    while cont:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cont = False
                pygame.quit()

        main()

if __name__ == "__main__":
    main()