import pygame

def draw_hp_bar(screen, x, y, hp, max_hp=7):
    """ HP를 시각적으로 표시하는 바 (10칸 초록색 블록) """
    bar_width = 20  # 한 칸의 너비
    bar_height = 10  # 높이
    spacing = 5  # 칸 사이의 간격

    for i in range(max_hp):
        color = (0, 255, 0) if i < hp else (100, 100, 100)  # HP가 남아있으면 초록색, 없으면 회색
        pygame.draw.rect(screen, color, (x + i * (bar_width + spacing), y, bar_width, bar_height))