import pygame
import sys
import random
from classes.player import Player
from classes.object import Crystal, Asteroid

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космический сборщик")
clock = pygame.time.Clock()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, SCREEN_WIDTH)

crystals = []
asteroids = []
spawn_timer = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-1)
    if keys[pygame.K_d]:
        player.move(1)
    
    spawn_timer += 1
    if spawn_timer  >= 30:
        spawn_timer = 0
        if random.random() < 0.6:
            crystals.append(Crystal(SCREEN_WIDTH))
        else: 
            asteroids.append(Asteroid(SCREEN_WIDTH))

    for crystal in crystals[:]:
        crystal.update()
        if crystal.is_off_screen(SCREEN_HEIGHT):
            crystals.remove(crystal)
    
    for asteroid in asteroids[:]:
        asteroid.update()
        if asteroid.is_off_screen(SCREEN_HEIGHT):
            asteroids.remove(asteroid)

    screen.fill((0, 0, 0)) 
    player.draw(screen)

    for crystal in crystals:
        crystal.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()