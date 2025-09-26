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
        super().__init__(x, -30, 25, 25, (0, 255, 150), 4)  
        self.points = 1

    def draw(self, screen):
        center_x, center_y = self.rect.center
        size = self.rect.width // 2

        points = [
            (center_x, center_y - size),  
            (center_x + size, center_y),  
            (center_x, center_y + size), 
            (center_x - size, center_y),  
        ]
        pygame.draw.polygon(screen, self.color, points)
        highlight_color = (200, 255, 200)
        pygame.draw.circle(
            screen,
            highlight_color,
            (center_x - size // 3, center_y - size // 3),
            size // 4,
        )


class Asteroid(FallingObject):
    def __init__(self, screen_width):
        x = random.randint(20, screen_width - 50)
        super().__init__(x, -30, 35, 35, (255, 100, 50), 3)
        self.damage = 1 

    def draw(self, screen):
        center_x, center_y = self.rect.center
        radius = self.rect.width // 2

        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)

        crater_color = (200, 80, 80)
        pygame.draw.circle(
            screen,
            crater_color,
            (center_x - radius // 3, center_y - radius // 3),
            radius // 4,
        )
        pygame.draw.circle(
            screen,
            crater_color,
            (center_x + radius // 3, center_y + radius // 3),
            radius // 5,
        )
