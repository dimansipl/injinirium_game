import pygame
import sys
import random
import time
from classes.player import Player
from classes.object import Crystal, Asteroid
from database.database_manager import GameDatabase

def init_game():
    pygame.init()
    
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    WINNING_SCORE = 2
    
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 20)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Космический сборщик")
    clock = pygame.time.Clock()
    
    db = GameDatabase()
    
    return SCREEN_WIDTH, SCREEN_HEIGHT, WINNING_SCORE, screen, clock, font, small_font, db

def get_name(screen, font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT, clock):
    player_name = ""
    input_text = ""
    taking_name = True
    
    while taking_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip():
                    player_name = input_text.strip()
                    taking_name = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode:
                    input_text += event.unicode
        
        screen.fill((0, 0, 0))
        text1 = font.render("Введите имя:", True, (255, 255, 255))
        text2 = font.render(input_text, True, (255, 255, 255))
        text3 = small_font.render("Нажмите ENTER", True, (200, 200, 200))

        screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, 250))
        screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, 300))
        screen.blit(text3, (SCREEN_WIDTH//2 - text3.get_width()//2, 350))

        pygame.display.flip()
        clock.tick(60)
    
    return player_name, True

def name_input():
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    
    if keys[pygame.K_a]: 
        dx -= 1
    if keys[pygame.K_d]: 
        dx += 1
    if keys[pygame.K_w]: 
        dy -= 1
    if keys[pygame.K_s]: 
        dy += 1
    
    return dx, dy

def update_objects(player, crystals, asteroids, SCREEN_HEIGHT, WINNING_SCORE):
    victory = False

    for crystal in crystals[:]:
        crystal.update()
        if crystal.rect.colliderect(player.rect):
            player.add_score(crystal.points)
            crystals.remove(crystal)
            if player.score >= WINNING_SCORE:
                victory = True
                return False, victory
        elif crystal.is_off_screen(SCREEN_HEIGHT):
            crystals.remove(crystal)

    for asteroid in asteroids[:]:
        asteroid.update()
        if asteroid.rect.colliderect(player.rect):
            if not player.take_damage(asteroid.damages):
                return False, victory 
            asteroids.remove(asteroid)
        elif asteroid.is_off_screen(SCREEN_HEIGHT):
            asteroids.remove(asteroid)
    
    return True, victory  

def draw_screen(screen, player, crystals, asteroids, player_name, game_time, font, SCREEN_WIDTH):
    screen.fill((0, 0, 0))

    player.draw(screen)
    for crystal in crystals:
        crystal.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

    minutes = int(game_time) // 60
    seconds = int(game_time) % 60
    milliseconds = int((game_time - int(game_time)) * 1000)
    
    time_text = font.render(f'Время: {minutes:02d}:{seconds:02d}:{milliseconds:03d}', True, (255, 255, 255))
    score_text = font.render(f'Очки: {player.score}', True, (255, 255, 255))
    lives_text = font.render(f'Жизни: {player.lives}', True, (255, 255, 255))
    name_text = font.render(f'Игрок: {player_name}', True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(name_text, (10, 50))
    screen.blit(time_text, (SCREEN_WIDTH - 250, 50))

def draw_screen_end(screen, victory, player, player_name, final_time, top_winners, font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT, WINNING_SCORE):
    screen.fill((20, 20, 40))

    minutes = int(final_time) // 60
    seconds = int(final_time) % 60
    milliseconds = int((final_time - int(final_time)) * 1000)
    
    if victory:
        game_over_text = font.render('Победа!', True, (50, 255, 50))
        score_text = font.render(f'Собрано кристаллов: {player.score}. ', True, (255, 255, 255))
        time_message = font.render(f'Время прохождения: {minutes:02d}:{seconds:02d}:{milliseconds:03d}', True, (255, 255, 255))
    else:
        game_over_text = font.render('ИГРА ОКОНЧЕНА!', True, (255, 150, 50))
        score_text = font.render(f'Собрано кристаллов: {player.score} Вы не собрали: {WINNING_SCORE - player.score}', True, (255, 255, 255))
        time_message = font.render(f'Вы продержались: {minutes:02d}:{seconds:02d}:{milliseconds:03d}', True, (255, 255, 255))
    
    restart = small_font.render('Пробел - новая игра', True, (200, 200, 200))

    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 50))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 100))
    screen.blit(time_message, (SCREEN_WIDTH//2 - time_message.get_width()//2, 150))
    screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, SCREEN_HEIGHT - 50))
    
    # Топ победителей
    top_title = font.render('Топ-5 победителей:', True, (255, 255, 255))
    screen.blit(top_title, (SCREEN_WIDTH//2 - top_title.get_width()//2, 250))
    
    if top_winners:
        for i, (name, score, time_val) in enumerate(top_winners):
            min_val = int(time_val) // 60
            sec_val = int(time_val) % 60
            ms_val = int((time_val - int(time_val)) * 1000)
            player_text = small_font.render(f'{i+1}. {name}: {min_val:02d}:{sec_val:02d}.{ms_val:03d}', True, (255, 255, 255))
            screen.blit(player_text, (SCREEN_WIDTH//2 - player_text.get_width()//2, 300 + i * 30))
    else:
        no_winners = font.render('Пока нет победителей', True, (200, 200, 200))
        screen.blit(no_winners, (SCREEN_WIDTH//2 - no_winners.get_width()//2, 300))

def main():

    SCREEN_WIDTH, SCREEN_HEIGHT, WINNING_SCORE, screen, clock, font, small_font, db = init_game()
    running = True
    
    while running:
        player_name, continue_running = get_name(screen, font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT, clock)
        if not continue_running:
            break

        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, SCREEN_WIDTH, SCREEN_HEIGHT)
        crystals = []
        asteroids = []
        spawn_timer = 0
        game_active = True
        victory = False
        
        start_time = time.time()

        while game_active and running:
            game_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_active = False

            dx, dy = name_input()
            player.move(dx, dy)

            spawn_timer += 1
            if spawn_timer >= 30:
                spawn_timer = 0
                if random.random() < 0.6:
                    crystals.append(Crystal(SCREEN_WIDTH))
                else: 
                    asteroids.append(Asteroid(SCREEN_WIDTH))

            game_active, victory = update_objects(player, crystals, asteroids, SCREEN_HEIGHT, WINNING_SCORE)

            draw_screen(screen, player, crystals, asteroids, player_name, game_time, font, SCREEN_WIDTH)
            pygame.display.flip()
            clock.tick(60)

        if running:
            final_time = time.time() - start_time

            if victory:
                db.save_winner(player_name, player.score, final_time)

            top_winners = db.get_top_winners()
            waiting = True
            
            while waiting and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting = False
                
                draw_screen_end(screen, victory, player, player_name, final_time, top_winners,
                                    font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT, WINNING_SCORE)
                pygame.display.flip()
                clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()