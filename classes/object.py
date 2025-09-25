import pygame
import random

class FallingObject:
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_off_screen(self, screen_height):
        return self.rect.top > screen_height

class Crystal(FallingObject):
    def __init__(self, screen_width):
        x = random.randint(20, screen_width - 40)
        super().__init__(x, -30, 20, 20, (0, 255, 0), 5)  # Зеленый
        self.points = 1

class Asteroid(FallingObject):
    def __init__(self, screen_width):
        x = random.randint(20, screen_width - 50)
        super().__init__(x, -30, 30, 30, (255, 0, 0), 5)  # Красный
        self.damages = 1