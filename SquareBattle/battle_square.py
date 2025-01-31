import pygame
import random
import math
from settings import WHITE, WIDTH, HEIGHT

class BattleSquare:
    def __init__(self, x, y, size, color, speed, hp):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.angle = random.uniform(0, 360)  # 초기 이동 방향 랜덤
        self.hp = hp
        self.spikes = {"top": False, "bottom": False, "left": False, "right": False}  # 초기 상태: 가시 없음
        self.spike_count = 0  # 몇 번 가시 요소를 먹었는지 추적

    def move(self):
        """사각형 이동 및 벽 충돌 처리"""
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.change_direction()
        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.change_direction()

    def change_direction(self):
        """충돌 시 랜덤한 방향으로 튕기기 (속도는 유지)"""
        self.angle += random.uniform(120, 240)  # 반사각 변경 (120~240도 랜덤)
        self.angle %= 360  # 360도 범위 유지

    def draw(self, screen):
        """사각형과 가시를 그림"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        self.draw_spikes(screen)

    def draw_spikes(self, screen):
        """가시를 각 변에 그리기"""
        spike_size = self.size // 5  # 가시 크기
        num_spikes = self.size // spike_size  # 가시 개수

        for i in range(num_spikes):
            if self.spikes["top"]:
                spike_x = self.x + i * spike_size
                spike_y = self.y
                pygame.draw.polygon(screen, WHITE, [
                    (spike_x, spike_y),
                    (spike_x + spike_size, spike_y),
                    (spike_x + spike_size // 2, spike_y - spike_size)
                ])
            if self.spikes["bottom"]:
                spike_x = self.x + i * spike_size
                spike_y = self.y + self.size
                pygame.draw.polygon(screen, WHITE, [
                    (spike_x, spike_y),
                    (spike_x + spike_size, spike_y),
                    (spike_x + spike_size // 2, spike_y + spike_size)
                ])

    def check_spike_collision(self, spike_item):
        """가시 요소와 충돌 감지 및 가시 추가"""
        if spike_item.exists and (
            self.x < spike_item.x < self.x + self.size and
            self.y < spike_item.y < self.y + self.size
        ):
            spike_item.exists = False  # 가시 요소 사라짐

            # 첫 번째 충돌: 상하에 가시 추가
            if self.spike_count == 0:
                self.spikes["top"] = True
                self.spikes["bottom"] = True
            # 두 번째 충돌: 좌우에 가시 추가
            elif self.spike_count == 1:
                self.spikes["left"] = True
                self.spikes["right"] = True

            self.spike_count += 1  # 가시 먹은 횟수 증가