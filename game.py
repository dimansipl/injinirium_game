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

running = True

while running:
    player_name = ""
    input_text = ""
    taking_name = True
    while taking_name and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                taking_name = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip():
                    player_name = input_text.strip()
                    taking_name = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode:
                    input_text += event.unicode
        screen.fill((0,0,0))
        text1 = font.render("Введите имя:", True, (255,255,255))
        text2 = font.render(input_text, True, (255,255,255))
        text3 = small_font.render("Нажмите ENTER", True, (200,200,200))

        screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, 250))
        screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, 300))
        screen.blit(text3, (SCREEN_WIDTH//2 - text3.get_width()//2, 350))

        pygame.display.flip()
        clock.tick(60)
    
    if not running:
        break

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, SCREEN_WIDTH)
    crystals = []
    asteroids = []
    spawn_timer = 0
    game_active = True

    while game_active and running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
    
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

        pygame.display.flip()
        clock.tick(60)


    if running:
        db.save_score(player_name, player.score)
        waiting = True
        while waiting and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

            screen.fill((20,20,40))
            game_over_text = font.render('ИГРА ОКОНЧЕНА!', True, (255, 150, 50))
            score_text = font.render(f'Ваш счет: {player.score} ', True, (255, 255,255))
            restart = small_font.render(f'Пробел - новая игра', True, (200,200,200))

            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 100))
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 150))
            screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, SCREEN_HEIGHT - 50))
            # Топ-5 игроков из базы данных
            top_players = db.get_top_scores()
            top_title = font.render('Топ-5 игроков:', True, (255, 255, 255))
            screen.blit(top_title, (SCREEN_WIDTH//2 - top_title.get_width()//2, 250))
            
            for i, (name, score) in enumerate(top_players):
                player_text = font.render(f'{i+1}. {name}: {score} очков', True, (255, 255, 255))
                screen.blit(player_text, (SCREEN_WIDTH//2 - player_text.get_width()//2, 300 + i * 30))
            
            pygame.display.flip()
            clock.tick(60)

pygame.quit()
sys.exit()