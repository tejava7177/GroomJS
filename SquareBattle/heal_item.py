import pygame
import random
from settings import WIDTH, HEIGHT, YELLOW

class HealItem:
    def __init__(self):
        """ Heal 아이템을 랜덤한 위치에 생성 """
        self.size = 25  # 병원 아이템 크기
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.color = (255, 0, 0)  # 빨간색 (병원 십자 모양)

    def draw(self, screen):
        """ 병원 모양 (십자형) 그리기 """
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        bar_width = self.size // 3  # 십자 너비

        # 수직 막대
        pygame.draw.rect(screen, self.color, (center_x - bar_width // 2, self.y, bar_width, self.size))
        # 수평 막대
        pygame.draw.rect(screen, self.color, (self.x, center_y - bar_width // 2, self.size, bar_width))