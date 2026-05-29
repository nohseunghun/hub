import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 장애물 피하기 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 100)

# FPS
clock = pygame.time.Clock()
FPS = 60

# 플레이어
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 7

# 장애물
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 6
obstacles = []

# 점수
score = 0
font = pygame.font.SysFont("malgungothic", 35)
small_font = pygame.font.SysFont("malgungothic", 25)

# 게임 상태
running = True
game_over = False

# 장애물 생성 함수
def create_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    return [x, y]

# 충돌 체크
def check_collision(px, py, ox, oy):
    player_rect = pygame.Rect(px, py, player_size, player_size)
    obstacle_rect = pygame.Rect(ox, oy, obstacle_width, obstacle_height)
    return player_rect.colliderect(obstacle_rect)

# 시작 장애물
for _ in range(3):
    obstacles.append(create_obstacle())

# 메인 루프
while running:
    clock.tick(FPS)

    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 재시작
                    player_x = WIDTH // 2
                    score = 0
                    obstacle_speed = 6
                    obstacles = [create_obstacle() for _ in range(3)]
                    game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # 플레이어 이동
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # 장애물 이동
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed

            # 화면 아래로 나가면 다시 생성
            if obstacle[1] > HEIGHT:
                obstacle[0] = random.randint(0, WIDTH - obstacle_width)
                obstacle[1] = -obstacle_height
                score += 1

                # 난이도 증가
                if score % 5 == 0:
                    obstacle_speed += 0.5

            # 충돌 체크
            if check_collision(player_x, player_y, obstacle[0], obstacle[1]):
                game_over = True

        # 플레이어 그리기
        pygame.draw.rect(
            screen,
            BLUE,
            (player_x, player_y, player_size, player_size),
            border_radius=10
        )

        # 장애물 그리기
        for obstacle in obstacles:
            pygame.draw.rect(
                screen,
                RED,
                (obstacle[0], obstacle[1], obstacle_width, obstacle_height),
                border_radius=10
            )

        # 점수 표시
        score_text = font.render(f"점수: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        level_text = small_font.render(
            f"속도: {round(obstacle_speed, 1)}",
            True,
            GREEN
        )
        screen.blit(level_text, (20, 70))

    else:
        # 게임 오버 화면
        over_text = font.render("💀 게임 오버!", True, RED)
        retry_text = small_font.render(
            "R 키를 눌러 다시 시작",
            True,
            BLACK
        )
        final_score = small_font.render(
            f"최종 점수: {score}",
            True,
            BLUE
        )

        screen.blit(over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
        screen.blit(final_score, (WIDTH // 2 - 80, HEIGHT // 2 + 10))
        screen.blit(retry_text, (WIDTH // 2 - 130, HEIGHT // 2 + 60))

    pygame.display.update()

pygame.quit()
