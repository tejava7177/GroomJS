import pygame
import random
from settings import WIDTH, HEIGHT, SPIKE_ITEM_SIZE, YELLOW

class SpikeItem:
    def __init__(self):
        """ 가시 아이템을 랜덤한 위치에 생성 """
        self.width = SPIKE_ITEM_SIZE
        self.height = SPIKE_ITEM_SIZE
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.color = YELLOW

    def draw(self, screen):
        """ 가시 아이템을 삼각형 모양으로 그리기 """
        spike_points = [
            (self.x, self.y + self.height),  # 왼쪽 아래
            (self.x + self.width // 2, self.y),  # 위쪽
            (self.x + self.width, self.y + self.height)  # 오른쪽 아래
        ]
        pygame.draw.polygon(screen, self.color, spike_points)