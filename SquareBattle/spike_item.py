import random
from settings import WIDTH, HEIGHT, YELLOW
import pygame

class SpikeItem:
    def __init__(self):
        self.size = 30
        self.exists = False  # 가시 요소 존재 여부

    def spawn(self):
        """랜덤 위치에 가시 요소 생성"""
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.exists = True

    def draw(self, screen):
        """가시 요소를 삼각형 모양으로 그림"""
        if self.exists:
            pygame.draw.polygon(screen, YELLOW, [
                (self.x, self.y),
                (self.x - self.size, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ])