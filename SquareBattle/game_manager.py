import pygame
import random
from validate_image_path import validate_image_path
from draw_hpBar import draw_hp_bar  # HP 바 UI 불러오기
from heal_item import HealItem  # HP 회복 아이템 추가
from settings import WIDTH, HEIGHT, FPS, WHITE, SPIKE_RESPAWN_TIME_RANGE
from battle_square import BattleSquare
from spike_item import SpikeItem
from additional_function.record import GameRecorder


def run_game():
    # ✅ Pygame 초기화
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle Square Game")
    clock = pygame.time.Clock()

    # ✅ 배경 음악 로드 및 재생
    pygame.mixer.init()
    pygame.mixer.music.load("/Users/simjuheun/Desktop/개인프로젝트/MadeGame/SquareBattle/additional_function/sounds/backgroundmusic.mid")  # ✅ 배경 음악 파일 경로
    pygame.mixer.music.set_volume(0.5)  # ✅ 볼륨 조절 (0.0 ~ 1.0)
    pygame.mixer.music.play(-1)  # ✅ 무한 반복 재생


    # ✅ 녹화 객체 생성 및 녹화 시작
    # recorder = GameRecorder(screen)
    # recorder.start_recording()



    # ✅ 이미지 경로를 코드 내에서 직접 지정
    red_image_path = "/Users/simjuheun/Downloads/About_WildBird-mobile1.jpg"
    blue_image_path = "/Users/simjuheun/Downloads/d0d236718ee188ca9c3c8999504d22501.jpg"

    # ✅ 예외 처리 함수 사용 (중복 제거)
    red_image_path = validate_image_path(red_image_path, "빨간색 사각형")
    blue_image_path = validate_image_path(blue_image_path, "파란색 사각형")

    # ✅ 사각형 객체 생성 (이미지 포함)
    red_square = BattleSquare(x=100, y=200, color=(255, 0, 0), controls="auto", image_path=red_image_path)
    blue_square = BattleSquare(x=600, y=200, color=(0, 0, 255), controls="auto", image_path=blue_image_path)

    # 가시 아이템 (초기에는 None, 이후 랜덤 생성)
    spike_item = None
    spike_spawn_timer = random.randint(*SPIKE_RESPAWN_TIME_RANGE)

    # Heal 아이템 (초기에는 None, 이후 랜덤 생성)
    heal_item = None
    heal_spawn_timer = random.randint(600, 1200)  # Heal 아이템 생성 텀 (10~20초)

    running = True
    while running:
        screen.fill(WHITE)

        # ✅ 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # ✅ 사각형 이동
        red_square.move()
        blue_square.move()

        # ✅ 사각형끼리 충돌 감지 및 반응
        if red_square.handle_collision(blue_square):  # ✅ 충돌 감지 시
            print("🚀 충돌이 감지되었습니다!")

        # ✅ 가시 아이템 생성 (랜덤 타이밍)
        if spike_item is None and spike_spawn_timer <= 0:
            spike_item = SpikeItem()
            spike_spawn_timer = random.randint(*SPIKE_RESPAWN_TIME_RANGE)  # 새로운 타이머 설정
        elif spike_item is None:
            spike_spawn_timer -= 1  # 가시 아이템 생성 타이머 감소

        # ✅ 가시 아이템이 존재하면 화면에 그림
        if spike_item:
            spike_item.draw(screen)

            # 가시 아이템 충돌 체크
            if red_square.check_spike_collision(spike_item):
                red_square.add_spike()
                spike_item = None  # 가시 아이템 제거
            elif blue_square.check_spike_collision(spike_item):
                blue_square.add_spike()
                spike_item = None  # 가시 아이템 제거

        # ✅ Heal 아이템 생성 로직 수정
        if heal_item is None and heal_spawn_timer <= 0:
            heal_item = HealItem()
            heal_spawn_timer = random.randint(900, 1500)  # Heal 아이템은 가시 아이템보다 더 늦게 생성됨
        elif heal_item is None:
            heal_spawn_timer -= 1  # Heal 아이템 생성 타이머 감소

        # ✅ Heal 아이템이 존재하면 화면에 그림
        if heal_item:
            heal_item.draw(screen)

            # Heal 아이템 충돌 체크
            if red_square.check_heal_collision(heal_item):
                red_square.heal(20)
                heal_item = None  # Heal 아이템 제거
            elif blue_square.check_heal_collision(heal_item):
                blue_square.heal(20)
                heal_item = None  # Heal 아이템 제거

        # ✅ 사각형 그리기
        red_square.draw(screen)
        blue_square.draw(screen)

        # ✅ HP 바 그리기
        draw_hp_bar(screen, 20, 20, red_square.hp // 10)  # 빨간 사각형 HP (왼쪽 상단)
        draw_hp_bar(screen, WIDTH - 260, 20, blue_square.hp // 10)  # 파란 사각형 HP (오른쪽 상단)

        # ✅ 승패 체크
        if red_square.hp <= 0:
            print("Blue Wins!")
            running = False
        elif blue_square.hp <= 0:
            print("Red Wins!")
            running = False


        pygame.display.flip()
        #recorder.capture_frame()      # ✅ 프레임을 기록
        clock.tick(FPS)

    #recorder.stop_recording()
    pygame.quit()