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
        new_x = self.x + self.speed * math.cos(math.radians(self.angle))
        new_y = self.y + self.speed * math.sin(math.radians(self.angle))

        # 벽 충돌 감지 후 위치 조정
        if new_x <= 0:
            self.angle = random.uniform(30, 150)  # 왼쪽 벽 충돌 → 무작위 방향 반사
            new_x = 1  # 벽과 겹치지 않도록 조정
        elif new_x + self.size >= WIDTH:
            self.angle = random.uniform(210, 330)  # 오른쪽 벽 충돌 → 무작위 방향 반사
            new_x = WIDTH - self.size - 1

        if new_y <= 0:
            self.angle = random.uniform(120, 240)  # 위쪽 벽 충돌 → 무작위 방향 반사
            new_y = 1
        elif new_y + self.size >= HEIGHT:
            self.angle = random.uniform(-60, 60)  # 아래쪽 벽 충돌 → 무작위 방향 반사
            new_y = HEIGHT - self.size - 1

        # 위치 업데이트
        self.x = new_x
        self.y = new_y

    def check_square_collision(self, other):
        """사각형끼리 충돌 감지 및 즉시 반응"""
        if (
            self.x < other.x + other.size and
            self.x + self.size > other.x and
            self.y < other.y + other.size and
            self.y + self.size > other.y
        ):
            # **충돌 후 강제 이동하여 겹침 방지**
            self.angle = random.uniform(0, 360)
            other.angle = random.uniform(0, 360)

            # 충돌 후 서로 반대 방향으로 밀어내기
            while (
                self.x < other.x + other.size and
                self.x + self.size > other.x and
                self.y < other.y + other.size and
                self.y + self.size > other.y
            ):
                self.x += self.speed * math.cos(math.radians(self.angle))
                self.y += self.speed * math.sin(math.radians(self.angle))
                other.x += other.speed * math.cos(math.radians(other.angle))
                other.y += other.speed * math.sin(math.radians(other.angle))

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