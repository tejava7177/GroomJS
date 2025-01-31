import pygame
import random
from settings import WIDTH, HEIGHT, SQUARE_SIZE, SQUARE_SPEED, INITIAL_HP

class BattleSquare:
    def __init__(self, x, y, color, controls="auto"):
        self.x = x
        self.y = y
        self.color = color
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE
        self.hp = INITIAL_HP
        self.speed_x = SQUARE_SPEED * random.choice([-1, 1])
        self.speed_y = SQUARE_SPEED * random.choice([-1, 1])
        self.spikes = {"top": False, "bottom": False, "left": False, "right": False}

    def move(self):
        """ 사각형 이동 처리 (벽에 부딪히면 단순 반사, 사각형끼리 충돌하면 랜덤 반사) """
        self.x += self.speed_x
        self.y += self.speed_y

        # 벽에 부딪히면 단순히 반대 방향으로 변경
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.speed_x *= -1  # 좌우 반사
        if self.y <= 0 or self.y + self.height >= HEIGHT:
            self.speed_y *= -1  # 상하 반사

    def random_bounce(self):
        """ 랜덤한 방향으로 튕기기 """
        self.speed_x = SQUARE_SPEED * random.choice([-1, 1])
        self.speed_y = SQUARE_SPEED * random.choice([-1, 1])

    def draw(self, screen):
        """ 사각형을 그리는 함수 """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        self.draw_spikes(screen)

    def draw_spikes(self, screen):
        """ 가시를 특정 변에 그리는 함수 """
        spike_color = (0, 0, 0)  # 가시는 검은색

        def draw_spike_line(start_x, start_y, end_x, end_y, direction):
            spike_width = self.width // 10  # 가시 간격
            for i in range(10):
                if direction == "horizontal":
                    spike_x = start_x + i * spike_width
                    pygame.draw.polygon(screen, spike_color, [
                        (spike_x, start_y),
                        (spike_x + spike_width // 2, end_y),
                        (spike_x + spike_width, start_y)
                    ])
                else:
                    spike_y = start_y + i * spike_width
                    pygame.draw.polygon(screen, spike_color, [
                        (start_x, spike_y),
                        (end_x, spike_y + spike_width // 2),
                        (start_x, spike_y + spike_width)
                    ])

        if self.spikes["top"]:
            draw_spike_line(self.x, self.y, self.x + self.width, self.y - 5, "horizontal")
        if self.spikes["bottom"]:
            draw_spike_line(self.x, self.y + self.height, self.x + self.width, self.y + self.height + 5, "horizontal")
        if self.spikes["left"]:
            draw_spike_line(self.x, self.y, self.x - 5, self.y + self.height, "vertical")
        if self.spikes["right"]:
            draw_spike_line(self.x + self.width, self.y, self.x + self.width + 5, self.y + self.height, "vertical")

    def add_spike(self):
        """ 사각형이 가시 아이템을 획득하면 가시 추가 및 랜덤 방향 변경 """
        if not self.spikes["top"] and not self.spikes["bottom"]:
            self.spikes["top"] = True
            self.spikes["bottom"] = True
        elif not self.spikes["left"] and not self.spikes["right"]:
            self.spikes["left"] = True
            self.spikes["right"] = True
        self.random_bounce()  # 가시를 얻었을 때도 랜덤 방향으로 튕기기

    def check_spike_collision(self, spike_item):
        """ 가시 아이템과 충돌했는지 확인 """
        spike_rect = pygame.Rect(spike_item.x, spike_item.y, spike_item.width, spike_item.height)
        my_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return my_rect.colliderect(spike_rect)

    def handle_collision(self, other):
        """ 상대 사각형과의 충돌 처리 """
        my_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        other_rect = pygame.Rect(other.x, other.y, other.width, other.height)

        if my_rect.colliderect(other_rect):
            # 가시 공격 판정
            if self.has_attacking_spike(other):
                other.hp -= 10
                # other.width = max(10, other.width - 2)  # 최소 크기 유지
                # other.height = max(10, other.height - 2)
                other.update_size()
                print(f"{self.color} 사각형이 공격! {other.color} HP: {other.hp}")

            # 충돌하면 랜덤한 방향으로 튕기기
            self.random_bounce()
            other.random_bounce()

    def has_attacking_spike(self, other):
        """ 상대방이 내 가시에 닿았는지 확인 """
        if self.spikes["top"] and other.y + other.height >= self.y and other.y < self.y:
            return True
        if self.spikes["bottom"] and other.y <= self.y + self.height and other.y > self.y:
            return True
        if self.spikes["left"] and other.x + other.width >= self.x and other.x < self.x:
            return True
        if self.spikes["right"] and other.x <= self.x + self.width and other.x > self.x:
            return True
        return False

    def update_size(self):
        """ HP가 10 감소할 때마다 크기 10% 감소, 속도 2% 증가 """
        scale_factor = 0.9  # 크기 10% 감소
        speed_factor = 1.02  # 속도 2% 증가

        self.width = max(10, int(self.width * scale_factor))  # 최소 크기 10 유지
        self.height = max(10, int(self.height * scale_factor))
        self.speed_x = int(self.speed_x * speed_factor) if self.speed_x != 0 else SQUARE_SPEED
        self.speed_y = int(self.speed_y * speed_factor) if self.speed_y != 0 else SQUARE_SPEED

        # 가시 크기도 사각형 크기에 맞게 줄이기
        self.draw_spikes_update()

    def draw_spikes_update(self):
        """ 가시 크기를 사각형 크기에 맞게 조정 """
        spike_size = self.width // 10  # 사각형 크기에 맞게 가시 크기 재조정