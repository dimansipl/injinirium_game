import pygame

class Player:
    def __init__(self, x, y, screen_width):
        self.rect = pygame.Rect(x, y, 50, 30)
        self.screen_width = screen_width
        self.speed = 8
        self.color = (0, 0, 255)  # Синий цвет

    def move(self, direction):
        self.rect.x += direction * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
