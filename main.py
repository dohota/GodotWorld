import pygame
import random
import math

# =====================
# 基础配置
# =====================
TILE_SIZE = 12
MAP_W, MAP_H = 50, 50
SCREEN_W = MAP_W * TILE_SIZE
SCREEN_H = MAP_H * TILE_SIZE

UNIT_RADIUS = 4
MOVE_RANGE = 2
ATTACK_RANGE = 5
DAMAGE = 3

BLUE = (80, 160, 255)
RED = (220, 80, 80)
GRID_COLOR = (40, 40, 40)
BG_COLOR = (20, 20, 20)

# =====================
# 单位数据（纯数据）
# =====================
class Unit:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.hp = 10

# =====================
# System：移动
# =====================
def movement_system(units):
    for u in units:
        dx = random.randint(-MOVE_RANGE, MOVE_RANGE)
        dy = random.randint(-MOVE_RANGE, MOVE_RANGE)
        u.x = max(0, min(MAP_W - 1, u.x + dx))
        u.y = max(0, min(MAP_H - 1, u.y + dy))

# =====================
# System：战斗
# =====================
def combat_system(units):
    for u in units:
        for v in units:
            if u.team == v.team:
                continue
            dist = math.hypot(u.x - v.x, u.y - v.y)
            if dist <= ATTACK_RANGE:
                v.hp -= DAMAGE

# =====================
# System：清理死亡单位
# =====================
def cleanup_system(units):
    return [u for u in units if u.hp > 0]

# =====================
# System：渲染
# =====================
def render(screen, units):
    screen.fill(BG_COLOR)

    # 画网格
    for x in range(MAP_W):
        pygame.draw.line(
            screen, GRID_COLOR,
            (x * TILE_SIZE, 0),
            (x * TILE_SIZE, SCREEN_H)
        )
    for y in range(MAP_H):
        pygame.draw.line(
            screen, GRID_COLOR,
            (0, y * TILE_SIZE),
            (SCREEN_W, y * TILE_SIZE)
        )

    # 画单位
    for u in units:
        color = BLUE if u.team == 0 else RED
        px = u.x * TILE_SIZE + TILE_SIZE // 2
        py = u.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, color, (px, py), UNIT_RADIUS)

# =====================
# 主程序
# =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Turn-Based Wargame Demo")

    clock = pygame.time.Clock()

    # 初始化单位
    units = []
    for _ in range(10):
        units.append(Unit(random.randint(0, 10), random.randint(0, MAP_H - 1), 0))
        units.append(Unit(random.randint(MAP_W - 11, MAP_W - 1), random.randint(0, MAP_H - 1), 1))

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 一回合结算
                    movement_system(units)
                    combat_system(units)
                    units = cleanup_system(units)
                    print(f"回合结束，单位数：{len(units)}")

        render(screen, units)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
