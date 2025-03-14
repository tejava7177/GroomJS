import pygame
import random
import math
import time
from settings import WIDTH, HEIGHT, SQUARE_SIZE, SQUARE_SPEED, INITIAL_HP, INITIAL_SLOW_DURATION, SLOW_SPEED_FACTOR

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
        self.start_time = time.time()  # ✅ 게임 시작 시간 기록(속도 조절을 위해서)

        # ✅ 이미지 로드 및 크기 조절 (사각형보다 작게)
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.scale_image()
            except pygame.error as e:
                print(f"이미지 로드 오류: {image_path} - {e}")
                self.image = None  # 오류 발생 시 기본 사각형 유지

    def has_spike(self):
        """ 사각형이 가시를 가지고 있는지 확인하는 메서드 """
        return any(self.spikes.values())  # ✅ 하나라도 True이면 가시가 있는 것

    def add_spike(self):
        """ 가시를 획득하면 네 개의 변 모두에 가시 추가 """
        self.spikes = {"top": True, "bottom": True, "left": True, "right": True}
        print(f"🦔 {self.color} 사각형이 가시를 얻음!")

    def remove_spikes(self):
        """ 공격 후 가시를 모두 제거 """
        self.spikes = {"top": False, "bottom": False, "left": False, "right": False}
        print(f"❌ {self.color} 사각형의 가시가 사라졌습니다!")



    def scale_image(self):
        """ 이미지 크기를 사각형 대비 80% 크기로 조정 """
        if self.image:
            img_width = int(self.width * 0.8)
            img_height = int(self.height * 0.8)
            self.image = pygame.transform.scale(self.image, (img_width, img_height))


    def move(self):
        """ 사각형 이동 처리 (벽 충돌 시 자연스러운 반사 및 떨림 방지) """
        # ✅ 게임 시작 후 3초 동안 속도 감소 적용
        elapsed_time = time.time() - self.start_time  # 현재 시간 - 게임 시작 시간
        speed_factor = SLOW_SPEED_FACTOR if elapsed_time < (INITIAL_SLOW_DURATION / 60) else 1  # 3초 후 정상 속도

        self.x += self.speed_x * speed_factor
        self.y += self.speed_y * speed_factor

        # ✅ 좌우 벽 충돌 처리
        if self.x <= 0:  # 왼쪽 벽 충돌
            self.x = 1
            self.speed_x *= -1
            self.speed_y += random.uniform(-0.3, 0.3)

        elif self.x + self.width >= WIDTH:  # 오른쪽 벽 충돌
            self.x = WIDTH - self.width - 1
            self.speed_x *= -1
            self.speed_y += random.uniform(-0.3, 0.3)

        # ✅ 상하 벽 충돌 처리
        if self.y <= 0:  # 위쪽 벽 충돌
            self.y = 1
            self.speed_y *= -1
            self.speed_x += random.uniform(-0.3, 0.3)

        elif self.y + self.height >= HEIGHT:  # 아래쪽 벽 충돌
            self.y = HEIGHT - self.height - 1
            self.speed_y *= -1
            self.speed_x += random.uniform(-0.3, 0.3)

        # ✅ 너무 작은 속도 방지 (벽에 붙어서 멈추는 문제 해결)
        min_speed = 1.5  # 최소 속도
        if abs(self.speed_x) < min_speed:
            self.speed_x = min_speed * (1 if self.speed_x > 0 else -1)
        if abs(self.speed_y) < min_speed:
            self.speed_y = min_speed * (1 if self.speed_y > 0 else -1)
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
        print(f"🦔 {self.color} 사각형이 가시를 얻음! 현재 가시 상태: {self.spikes}")
        #self.random_bounce()  # 가시를 얻었을 때도 랜덤 방향으로 튕기기

    def check_spike_collision(self, spike_item):
        """ 가시 아이템과 충돌했는지 확인 """
        spike_rect = pygame.Rect(spike_item.x, spike_item.y, spike_item.width, spike_item.height)
        my_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return my_rect.colliderect(spike_rect)


    def handle_collision(self, other):
        """ 상대 사각형과의 충돌 처리 (한 번만 실행) """
        my_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        other_rect = pygame.Rect(other.x, other.y, other.width, other.height)

        # ✅ 두 사각형의 중심 좌표 계산
        my_center_x, my_center_y = self.x + self.width / 2, self.y + self.height / 2
        other_center_x, other_center_y = other.x + other.width / 2, other.y + other.height / 2

        # ✅ 두 사각형 간의 거리 계산
        distance = math.sqrt((my_center_x - other_center_x) ** 2 + (my_center_y - other_center_y) ** 2)
        collision_threshold = (self.width + other.width) / 2 * 0.9  # 90% 크기 내에서 충돌 감지

        # ✅ 충돌 감지
        if my_rect.colliderect(other_rect) or distance < collision_threshold:
            print(f"🔍 {self.color} 사각형 & {other.color} 사각형 충돌 감지!")

            # ✅ 공격 판정 (양방향)
            if self.has_attacking_spike(other):
                other.hp -= 10
                other.update_size()
                print(f"💥 {self.color} 사각형이 공격! {other.color} HP: {other.hp}")
                self.remove_spikes()

            if other.has_attacking_spike(self):
                self.hp -= 10
                self.update_size()
                print(f"💥 {other.color} 사각형이 공격! {self.color} HP: {self.hp}")
                other.remove_spikes()

            # ✅ 겹침 방지 (양쪽 밀어내기)
            overlap_x = (self.width + other.width) / 40
            overlap_y = (self.height + other.height) / 40

            if self.x < other.x:
                self.x -= overlap_x
                other.x += overlap_x
            else:
                self.x += overlap_x
                other.x -= overlap_x

            if self.y < other.y:
                self.y -= overlap_y
                other.y += overlap_y
            else:
                self.y += overlap_y
                other.y -= overlap_y

            # ✅ 충돌하면 랜덤한 방향으로 튕기기
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


    # 수정한 후
    def update_size(self):
        """ HP 변화에 따라 크기를 조절 (줄어들고, 다시 커질 수 있음) """
        scale_factor = self.hp / INITIAL_HP  # 현재 HP 비율 계산

        # ✅ HP 비율에 따라 크기 조정 (최소 크기 10 유지)
        self.width = max(10, int(SQUARE_SIZE * scale_factor))
        self.height = max(10, int(SQUARE_SIZE * scale_factor))

        # ✅ 이동 속도도 HP 비율에 따라 조정 (최대 HP일 때 기본 속도로)
        self.speed_x = max(1, int(SQUARE_SPEED * (1 + (1 - scale_factor))))  # HP 줄어들수록 속도 증가
        self.speed_y = max(1, int(SQUARE_SPEED * (1 + (1 - scale_factor))))

        # ✅ 이미지 크기 조정
        self.scale_image()

        # ✅ 가시 크기도 사각형 크기에 맞게 줄이기
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
        """ HP 회복 (최대 100 제한) 및 크기 복구 -> 70으로 수정 """
        previous_hp = self.hp  # ✅ 회복 전 HP 저장
        self.hp = min(INITIAL_HP, self.hp + amount)  # ✅ HP 회복

        if self.hp > previous_hp:  # ✅ HP가 증가한 경우 크기도 원래 크기로 증가
            self.update_size()

        print(f"💚 {self.color} 사각형이 HP {amount} 회복! 현재 HP: {self.hp}")

    def scale_image(self):
        """ 이미지 크기를 현재 사각형 크기에 맞게 조정 """
        if self.image:
            img_width = int(self.width * 0.8)  # 사각형의 80% 크기로 설정
            img_height = int(self.height * 0.8)
            self.image = pygame.transform.scale(self.image, (img_width, img_height))
