import pygame


class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.rect = pygame.Rect(x, y, 50, 40)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 8
        self.color = (100, 150, 255) 
        self.score = 0
        self.lives = 3  

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def draw(self, screen):
        points = [
            (self.rect.centerx, self.rect.top),  
            (self.rect.left, self.rect.bottom),  
            (self.rect.right, self.rect.bottom), 
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.circle(
            screen, (200, 200, 255), (self.rect.centerx, self.rect.centery), 8
        )

        engine_color = (255, 100, 100)
        pygame.draw.rect(
            screen, engine_color, (self.rect.centerx - 6, self.rect.bottom - 5, 12, 8)
        )

    def add_score(self, points):
        self.score += points

    def take_damage(self, damage=1):
        self.lives -= damage
        return self.lives > 0
