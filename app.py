import pygame
import random
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 SPACE SURVIVAL")

clock = pygame.time.Clock()
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 70, 70)
BLUE = (80, 170, 255)
YELLOW = (255, 220, 0)
GREEN = (0, 255, 120)
PURPLE = (180, 0, 255)

# 폰트
font = pygame.font.SysFont("arial", 32)
big_font = pygame.font.SysFont("arial", 64)
small_font = pygame.font.SysFont("arial", 22)

# 플레이어
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 7
player_hp = 100

# 총알
bullets = []
bullet_speed = 10

# 적
enemies = []
enemy_speed = 3
spawn_timer = 0

# 별 배경
stars = []
for _ in range(100):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 4)
    ])

# 점수
score = 0
wave = 1

# 폭발 효과
explosions = []

# 게임 상태
running = True
game_over = False

# 적 생성
class Enemy:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50
        self.size = random.randint(35, 60)
        self.speed = enemy_speed + random.random() * 2
        self.hp = self.size // 10

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size // 4)

# 폭발 클래스
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.life = 20

    def update(self):
        self.radius += 3
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius, 3)

# 플레이어 그리기

def draw_player(x, y):
    pygame.draw.polygon(screen, BLUE, [
        (x, y),
        (x - 20, y + 50),
        (x + 20, y + 50)
    ])

    pygame.draw.rect(screen, WHITE, (x - 5, y + 10, 10, 20))

# 거리 계산

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 메인 루프
while running:
    clock.tick(FPS)

    # 배경
    screen.fill(BLACK)

    # 별 애니메이션
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        star[1] += star[2]

        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

    # 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append([player_x, player_y])

            if event.key == pygame.K_r and game_over:
                # 게임 리셋
                player_hp = 100
                score = 0
                wave = 1
                enemy_speed = 3
                enemies.clear()
                bullets.clear()
                explosions.clear()
                game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # 플레이어 이동
        if keys[pygame.K_LEFT] and player_x > 30:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH - 30:
            player_x += player_speed

        if keys[pygame.K_UP] and player_y > 50:
            player_y -= player_speed

        if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
            player_y += player_speed

        # 적 생성
        spawn_timer += 1

        if spawn_timer > max(20, 60 - wave * 2):
            enemies.append(Enemy())
            spawn_timer = 0

        # 총알 이동
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed

            pygame.draw.rect(screen, GREEN, (bullet[0], bullet[1], 5, 15))

            if bullet[1] < 0:
                bullets.remove(bullet)

        # 적 이동
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw()

            # 플레이어 충돌
            if distance(player_x, player_y, enemy.x, enemy.y) < enemy.size:
                player_hp -= 20
                explosions.append(Explosion(int(enemy.x), int(enemy.y)))
                enemies.remove(enemy)

                if player_hp <= 0:
                    game_over = True

            # 화면 밖 제거
            elif enemy.y > HEIGHT + 50:
                enemies.remove(enemy)

            # 총알 충돌
            for bullet in bullets[:]:
                if distance(bullet[0], bullet[1], enemy.x, enemy.y) < enemy.size // 2:
                    enemy.hp -= 1

                    if bullet in bullets:
                        bullets.remove(bullet)

                    if enemy.hp <= 0:
                        explosions.append(Explosion(int(enemy.x), int(enemy.y)))

                        if enemy in enemies:
                            enemies.remove(enemy)

                        score += 10

                        if score % 100 == 0:
                            wave += 1
                            enemy_speed += 0.5

        # 폭발 업데이트
        for explosion in exp
