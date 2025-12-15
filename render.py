import math
import pygame
class RenderersSystem:
    def __init__(self, screen):
        self.screen = screen
        self.debugInfo = None  # JS 中是 DOM，这里保留接口含义

    def clear(self):
        self.screen.fill((0,0,0))

    def drawHexagon(self, x, y, size, color, strokeColor, lineWidth=1):
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg
            px = x + size * math.cos(angle_rad)
            py = y + size * math.sin(angle_rad)
            points.append((px, py))
        pygame.draw.polygon(self.screen, color, points) # 填充
        pygame.draw.polygon(self.screen, strokeColor, points, width=int(max(1, lineWidth))) # 描边

    def drawUnit(self, x, y, unit, zoom):
        # 阵营边框颜色
        teamColor = CONFIG.COLORS.P1 if unit.owner == 1 else CONFIG.COLORS.P2
        radius = CONFIG.HEX_SIZE * 0.6 * zoom
        # 单位主体
        pygame.draw.circle(
            self.screen,
            unit.color,
            (int(x), int(y)),
            int(radius)
        )
        # 阵营描边
        pygame.draw.circle(
            self.screen,
            teamColor,
            (int(x), int(y)),
            int(radius),
            width=int(4 * zoom)
        )
        # 单位文字
        if zoom > 0.6:
            font = pygame.font.SysFont(
                "Arial",
                int(14 * zoom),
                bold=True
            )
            text = font.render(unit.name[0], True, (255, 255, 255))
            rect = text.get_rect(center=(x, y))
            self.screen.blit(text, rect)

    def render(self, game, camera):
        self.clear()
        # --- 视锥剔除边界 ---
        padding = CONFIG.HEX_SIZE * 2 * camera.zoom
        viewBounds = {
            "left": -padding,
            "top": -padding,
            "right": self.screen.get_width() + padding,
            "bottom": self.screen.get_height() + padding
        }
        # --- 缓存缩放后的尺寸 ---
        hexRadius = (CONFIG.HEX_SIZE - 2) * camera.zoom
        selectRadius = (CONFIG.HEX_SIZE + 2) * camera.zoom
        renderedCount = 0
        # --- 绘制地图 ---
        for tile in game.map:
            worldPos = HexMath.hexToWorld(tile.q, tile.r)
            screenPos = camera.worldToScreen(worldPos["x"], worldPos["y"])
            # Culling
            if (screenPos["x"] < viewBounds["left"] or
                screenPos["x"] > viewBounds["right"] or
                screenPos["y"] < viewBounds["top"] or
                screenPos["y"] > viewBounds["bottom"]):
                continue
            renderedCount += 1
            color = CONFIG.COLORS.TILE
            if any(m.q == tile.q and m.r == tile.r for m in game.validMoves):
                color = CONFIG.COLORS.MOVE_HINT
            self.drawHexagon(
                screenPos["x"],
                screenPos["y"],
                hexRadius,
                color,
                CONFIG.COLORS.TILE_STROKE
            )
        # --- 绘制选中框 ---
        if game.selectedUnit:
            wPos = HexMath.hexToWorld(
                game.selectedUnit.q,
                game.selectedUnit.r
            )
            sPos = camera.worldToScreen(wPos["x"], wPos["y"])

            if viewBounds["left"] < sPos["x"] < viewBounds["right"]:
                self.drawHexagon(
                    sPos["x"],
                    sPos["y"],
                    selectRadius,
                    CONFIG.COLORS.HIGHLIGHT,
                    "gold",
                    2
                )

        # --- 绘制单位 ---
        for unit in game.units:
            wPos = HexMath.hexToWorld(unit.q, unit.r)
            sPos = camera.worldToScreen(wPos["x"], wPos["y"])

            if (sPos["x"] < viewBounds["left"] or
                sPos["x"] > viewBounds["right"] or
                sPos["y"] < viewBounds["top"] or
                sPos["y"] > viewBounds["bottom"]):
                continue

            self.drawUnit(
                sPos["x"],
                sPos["y"],
                unit,
                camera.zoom
            )
