import pygame
import sys
import random
from classes.player import Player
from classes.object import Crystal, Asteroid
from database.database_manager import GameDatabase

pygame.init()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 20)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космический сборщик")
clock = pygame.time.Clock()

db = GameDatabase()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, SCREEN_WIDTH)

crystals = []
asteroids = []
spawn_timer = 0


running = True
game_active = True

player_name = input()
name_input_active = False 


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_SPACE:
                db.save_score(player_name, player.score)

                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, SCREEN_WIDTH)
                crystals.clear()
                asteroids.clear()
                game_active = True

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
    name_text = font.render(f'Игрок: {player_name}', True, (255,255,255))

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(name_text, (10, 50))


    if not game_active:
        screen.fill((20,20,40))
        game_over_text = font.render('ИГРА ОКОНЧЕНА!', True, (255, 150, 50))
        score_text = font.render(f'Ваш счет: {player.score} ', True, (255, 255,255))

        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 150))
         # Топ-5 игроков из базы данных
        top_players = db.get_top_scores()
        top_title = font.render('Топ-5 игроков:', True, (255, 255, 255))
        screen.blit(top_title, (SCREEN_WIDTH//2 - top_title.get_width()//2, 250))
        
        for i, (name, score) in enumerate(top_players):
            player_text = font.render(f'{i+1}. {name}: {score} очков', True, (255, 255, 255))
            screen.blit(player_text, (SCREEN_WIDTH//2 - player_text.get_width()//2, 300 + i * 30))
        
        hint_text = small_font.render('Нажмите ПРОБЕЛ для новой игры', True, (150, 150, 150))
        screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 450))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()