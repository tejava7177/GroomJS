import pygame

# 화면 크기
WIDTH, HEIGHT = 550, 500

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # 가시 요소 색상

# FPS 설정
FPS = 60

# 초기 가시 요소 생성 타이머 (3초 이내)
INITIAL_SPAWN_TIME = 100  # 2~3초

# 사각형 기본 설정
INITIAL_HP = 100  # 사각형의 초기 HP (Power)
SQUARE_SIZE = 120  # 사각형 기본 크기
SQUARE_SPEED = 6  # 사각형 이동 속도

# 가시 요소 관련 설정
SPIKE_ITEM_SIZE = 25  # 가시 아이템 크기
#SPIKE_RESPAWN_TIME_RANGE = (60, 180)  # 1초 ~ 3초 (기존보다 빠르게)
SPIKE_RESPAWN_TIME = 120  # 2초마다 가시 요소 등장