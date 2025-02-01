import pygame
import random
from settings import WIDTH, HEIGHT, SQUARE_SIZE, SQUARE_SPEED, INITIAL_HP

class BattleSquare:
    def __init__(self, x, y, color, controls="auto" , image_path=None):
        self.x = x
        self.y = y
        self.color = color
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE
        self.hp = INITIAL_HP
        self.speed_x = SQUARE_SPEED * random.choice([-1, 1])
        self.speed_y = SQUARE_SPEED * random.choice([-1, 1])
        self.spikes = {"top": False, "bottom": False, "left": False, "right": False}
        self.image = None

        # ✅ 이미지 로드 및 크기 조절 (사각형보다 작게)
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.scale_image()
            except pygame.error as e:
                print(f"이미지 로드 오류: {image_path} - {e}")
                self.image = None  # 오류 발생 시 기본 사각형 유지

    def scale_image(self):
        """ 이미지 크기를 사각형 대비 80% 크기로 조정 """
        if self.image:
            img_width = int(self.width * 0.8)
            img_height = int(self.height * 0.8)
            self.image = pygame.transform.scale(self.image, (img_width, img_height))

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
        """ 사각형 내부에 이미지 배치 """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))  # 사각형 먼저 그림
        self.draw_spikes(screen)  # 가시를 사각형 위에 그림

        if self.image:
            # ✅ 이미지의 중앙 정렬 (사각형 내부)
            img_x = self.x + (self.width - self.image.get_width()) // 2
            img_y = self.y + (self.height - self.image.get_height()) // 2
            screen.blit(self.image, (img_x, img_y))  # 이미지 그리기

    def draw_spikes(self, screen):
        """ 가시를 사각형 바깥에 배치하여 이미지에 가려지지 않도록 설정 """
        spike_color = (0, 0, 0)  # 가시는 검은색
        spike_size = self.width // 10  # 가시 크기

        def draw_spike_line(start_x, start_y, end_x, end_y, direction):
            for i in range(10):
                if direction == "horizontal":
                    spike_x = start_x + i * spike_size
                    pygame.draw.polygon(screen, spike_color, [
                        (spike_x, start_y),
                        (spike_x + spike_size // 2, end_y),
                        (spike_x + spike_size, start_y)
                    ])
                else:
                    spike_y = start_y + i * spike_size
                    pygame.draw.polygon(screen, spike_color, [
                        (start_x, spike_y),
                        (end_x, spike_y + spike_size // 2),
                        (start_x, spike_y + spike_size)
                    ])

        if self.spikes["top"]:
            draw_spike_line(self.x, self.y - 5, self.x + self.width, self.y - 10, "horizontal")
        if self.spikes["bottom"]:
            draw_spike_line(self.x, self.y + self.height + 5, self.x + self.width, self.y + self.height + 10,
                            "horizontal")
        if self.spikes["left"]:
            draw_spike_line(self.x - 5, self.y, self.x - 10, self.y + self.height, "vertical")
        if self.spikes["right"]:
            draw_spike_line(self.x + self.width + 5, self.y, self.x + self.width + 10, self.y + self.height, "vertical")

            
    def add_spike(self):
        """ 가시 아이템을 획득하면 네 개의 변 모두에 가시 추가 """
        self.spikes["top"] = True
        self.spikes["bottom"] = True
        self.spikes["left"] = True
        self.spikes["right"] = True
        #self.random_bounce()  # 가시를 얻었을 때도 랜덤 방향으로 튕기기

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
                other.update_size()  # 크기 및 속도 업데이트
                print(f"{self.color} 사각형이 공격! {other.color} HP: {other.hp}")

                # 공격 성공 후 가시 제거
                self.remove_spikes()

            # 충돌하면 랜덤한 방향으로 튕기기
            self.random_bounce()
            other.random_bounce()
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
        speed_factor = 1.05  # 속도 5% 증가

        self.width = max(10, int(self.width * scale_factor))  # 최소 크기 10 유지
        self.height = max(10, int(self.height * scale_factor))
        self.speed_x = int(self.speed_x * speed_factor) if self.speed_x != 0 else SQUARE_SPEED
        self.speed_y = int(self.speed_y * speed_factor) if self.speed_y != 0 else SQUARE_SPEED

        # 가시 크기도 사각형 크기에 맞게 줄이기
        self.draw_spikes_update()

    def draw_spikes_update(self):
        """ 가시 크기를 사각형 크기에 맞게 조정 """
        spike_size = self.width // 10  # 사각형 크기에 맞게 가시 크기 재조정

    def remove_spikes(self):
        """ 공격 후 가시를 모두 제거 """
        self.spikes["top"] = False
        self.spikes["bottom"] = False
        self.spikes["left"] = False
        self.spikes["right"] = False
        print(f"{self.color} 사각형의 가시가 사라졌습니다!")

    def check_heal_collision(self, heal_item):
        """ Heal 아이템과 충돌했는지 확인 """
        heal_rect = pygame.Rect(heal_item.x, heal_item.y, heal_item.size, heal_item.size)
        my_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return my_rect.colliderect(heal_rect)

    def heal(self, amount):
        """ HP 회복 (최대 100 제한) """
        self.hp = min(100, self.hp + amount)
        print(f"{self.color} 사각형이 HP {amount} 회복! 현재 HP: {self.hp}")