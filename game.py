import pygame
import sys
import random
from classes.player import Player
from classes.object import Crystal, Asteroid

pygame.init()
font = pygame.font.SysFont(None, 36)
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
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game_active:
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
            if crystal.rect.colliderect(player.rect):
                player.add_score(crystal.points)
                crystals.remove(crystal)
                print(f"Собран кристалл! Очки: {player.score}")
            elif crystal.is_off_screen(SCREEN_HEIGHT):
                crystals.remove(crystal)
    
        for asteroid in asteroids[:]:
            asteroid.update()
            if asteroid.rect.colliderect(player.rect):
                if not player.take_damage(asteroid.damages):
                    game_active = False
                    print("Игра окончена")
                asteroids.remove(asteroid)
            elif asteroid.is_off_screen(SCREEN_HEIGHT):
                asteroids.remove(asteroid)

    screen.fill((0, 0, 0)) 
    player.draw(screen)

    for crystal in crystals:
        crystal.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    score_text = font.render(f'Очки: {player.score}', True, (255, 255, 255))
    lives_text = font.render(f'Жизни: {player.lives}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
    if not game_active:
        game_over_text = font.render('ИГРА ОКОНЧЕНА!', True, (255, 50, 50))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()