import pygame
from settings import *
from battle_square import BattleSquare
from spike_item import SpikeItem

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # 객체 생성
    square1 = BattleSquare(200, 300, 100, RED, 5, 100)
    square2 = BattleSquare(500, 300, 100, BLUE, 5, 100)
    spike_item = SpikeItem()

    frame_count = 0  # 프레임 카운트

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 사각형 이동
        square1.move()
        square2.move()

        # 3초 이내 가시 요소 첫 등장, 이후 계속 유지
        if frame_count >= INITIAL_SPAWN_TIME and not spike_item.exists:
            spike_item.spawn()

        # 충돌 감지
        square1.check_spike_collision(spike_item)
        square2.check_spike_collision(spike_item)

        # 사각형 및 가시 요소 그리기
        square1.draw(screen)
        square2.draw(screen)
        spike_item.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
        frame_count += 1  # 프레임 증가

    pygame.quit()