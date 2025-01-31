# import pygame
# import random
# import math
#
# # 초기 설정
# pygame.init()
#
# # 화면 크기
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Battle Squares")
#
# # 색상 정의
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)
# BLACK = (0, 0, 0)
# YELLOW = (255, 255, 0)  # 가시 요소 색상
#
# # FPS 설정
# clock = pygame.time.Clock()
# FPS = 60
#
# # 가시 요소 타이머 (3초 이내 생성)
# INITIAL_SPAWN_TIME = 180  # 3초 (60 FPS 기준)
# spike_timer = INITIAL_SPAWN_TIME
#
#
# # 가시 아이템 클래스
# class SpikeItem:
#     def __init__(self):
#         self.size = 30
#         self.exists = False  # 가시 요소 존재 여부
#
#     def spawn(self):
#         """랜덤 위치에 가시 요소 생성"""
#         self.x = random.randint(50, WIDTH - 50)
#         self.y = random.randint(50, HEIGHT - 50)
#         self.exists = True
#
#     def draw(self):
#         """가시 요소를 삼각형 모양으로 그림"""
#         if self.exists:
#             pygame.draw.polygon(screen, YELLOW, [
#                 (self.x, self.y),
#                 (self.x - self.size, self.y + self.size),
#                 (self.x + self.size, self.y + self.size)
#             ])
#
#
# # 사각형 클래스 정의
# class BattleSquare:
#     def __init__(self, x, y, size, color, speed, hp):
#         self.x = x
#         self.y = y
#         self.size = size
#         self.color = color
#         self.speed = speed
#         self.angle = random.uniform(0, 360)  # 초기 이동 방향 랜덤
#         self.hp = hp
#         self.spikes = {"top": False, "bottom": False, "left": False, "right": False}  # 초기 상태: 가시 없음
#         self.spike_count = 0  # 몇 번 가시 요소를 먹었는지 추적
#
#     def move(self):
#         """사각형 이동 및 벽 충돌 처리"""
#         self.x += self.speed * math.cos(math.radians(self.angle))
#         self.y += self.speed * math.sin(math.radians(self.angle))
#
#         if self.x <= 0 or self.x + self.size >= WIDTH:
#             self.change_direction()
#         if self.y <= 0 or self.y + self.size >= HEIGHT:
#             self.change_direction()
#
#     def change_direction(self):
#         """충돌 시 랜덤한 방향으로 튕기기 (속도는 유지)"""
#         self.angle += random.uniform(120, 240)  # 반사각 변경 (120~240도 랜덤)
#         self.angle %= 360  # 360도 범위 유지
#
#     def draw(self):
#         """사각형과 가시를 그림"""
#         pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
#         self.draw_spikes()
#
#     def draw_spikes(self):
#         """가시를 각 변에 그리기"""
#         spike_size = self.size // 5  # 가시 크기
#         num_spikes = self.size // spike_size  # 가시 개수
#
#         for i in range(num_spikes):
#             if self.spikes["top"]:
#                 spike_x = self.x + i * spike_size
#                 spike_y = self.y
#                 pygame.draw.polygon(screen, WHITE, [
#                     (spike_x, spike_y),
#                     (spike_x + spike_size, spike_y),
#                     (spike_x + spike_size // 2, spike_y - spike_size)
#                 ])
#             if self.spikes["bottom"]:
#                 spike_x = self.x + i * spike_size
#                 spike_y = self.y + self.size
#                 pygame.draw.polygon(screen, WHITE, [
#                     (spike_x, spike_y),
#                     (spike_x + spike_size, spike_y),
#                     (spike_x + spike_size // 2, spike_y + spike_size)
#                 ])
#             if self.spikes["left"]:
#                 spike_x = self.x
#                 spike_y = self.y + i * spike_size
#                 pygame.draw.polygon(screen, WHITE, [
#                     (spike_x, spike_y),
#                     (spike_x, spike_y + spike_size),
#                     (spike_x - spike_size, spike_y + spike_size // 2)
#                 ])
#             if self.spikes["right"]:
#                 spike_x = self.x + self.size
#                 spike_y = self.y + i * spike_size
#                 pygame.draw.polygon(screen, WHITE, [
#                     (spike_x, spike_y),
#                     (spike_x, spike_y + spike_size),
#                     (spike_x + spike_size, spike_y + spike_size // 2)
#                 ])
#
#     def check_spike_collision(self, spike_item):
#         """가시 요소와 충돌 감지 및 가시 추가"""
#         if spike_item.exists and (
#             self.x < spike_item.x < self.x + self.size and
#             self.y < spike_item.y < self.y + self.size
#         ):
#             spike_item.exists = False  # 가시 요소 사라짐
#
#             # 첫 번째 충돌: 상하에 가시 추가
#             if self.spike_count == 0:
#                 self.spikes["top"] = True
#                 self.spikes["bottom"] = True
#             # 두 번째 충돌: 좌우에 가시 추가
#             elif self.spike_count == 1:
#                 self.spikes["left"] = True
#                 self.spikes["right"] = True
#
#             self.spike_count += 1  # 가시 먹은 횟수 증가
#
#     def check_square_collision(self, other):
#         """사각형끼리 충돌 감지 및 공격 성공 시 가시 제거"""
#         if (
#             self.x < other.x + other.size and
#             self.x + self.size > other.x and
#             self.y < other.y + other.size and
#             self.y + self.size > other.y
#         ):
#             # 가시 공격 판정
#             for side in ["top", "bottom", "left", "right"]:
#                 if self.spikes[side]:  # 가시 공격 성공
#                     other.hp -= 10
#                     other.size -= 5
#                     if other.hp <= 0:
#                         other.size = 0  # HP 0이면 제거
#                     self.spikes = {"top": False, "bottom": False, "left": False, "right": False}  # 공격 성공 시 가시 제거
#
#             # 충돌 시 방향 변경
#             self.change_direction()
#             other.change_direction()
#
#
#
# # 사각형 및 가시 요소 생성
# square1 = BattleSquare(200, 300, 100, RED, 5, 100)
# square2 = BattleSquare(500, 300, 100, BLUE, 5, 100)
# spike_item = SpikeItem()
#
# # 게임 루프
# running = True
# frame_count = 0
#
# while running:
#     screen.fill(BLACK)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     square1.move()
#     square2.move()
#
#     # 3초 이내 가시 요소 첫 등장, 이후 항상 유지
#     if frame_count >= spike_timer and not spike_item.exists:
#         spike_item.spawn()
#
#     # 사각형과 가시 요소 충돌 감지
#     square1.check_spike_collision(spike_item)
#     square2.check_spike_collision(spike_item)
#
#     # 사각형끼리 충돌 감지
#     square1.check_square_collision(square2)
#
#     # 사각형 및 가시 요소 그리기
#     square1.draw()
#     square2.draw()
#     spike_item.draw()
#
#     pygame.display.flip()
#     clock.tick(FPS)
#     frame_count += 1  # 프레임 증가
#
# pygame.quit()