import pygame

# 화면 크기
WIDTH, HEIGHT = 800, 600

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # 가시 요소 색상

# FPS 설정
FPS = 60

# 초기 가시 요소 생성 타이머 (3초 이내)
INITIAL_SPAWN_TIME = 180  # 3초 (60 FPS 기준)

# 사각형 기본 설정
INITIAL_HP = 100  # 사각형의 초기 HP (Power)
SQUARE_SIZE = 50  # 사각형 기본 크기
SQUARE_SPEED = 3  # 사각형 이동 속도

# 가시 요소 관련 설정
SPIKE_ITEM_SIZE = 20  # 가시 아이템 크기
SPIKE_RESPAWN_TIME_RANGE = (180, 600)  # 가시 아이템 생성 대기 시간 범위 (3초~10초)