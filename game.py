import pygame
import sys
from classes.player import Player

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космический сборщик")
clock = pygame.time.Clock()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, SCREEN_WIDTH)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1)
    if keys[pygame.K_RIGHT]:
        player.move(1)
    
    screen.fill((0, 0, 0)) 
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()