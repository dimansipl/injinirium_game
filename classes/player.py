import pygame

class Player:
    def __init__(self, x, y, screen_width):
        self.rect = pygame.Rect(x, y, 50, 30)
        self.screen_width = screen_width
        self.speed = 8
        self.color = (0, 0, 255)  # Синий цвет
        self.score = 0
        self.lives = 3

    def move(self, direction):
        self.rect.x += direction * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def add_score(self, points):
        self.score += points

    def take_damage(self, damage = 1):
        self.lives -= damage
        return self.lives > 0
