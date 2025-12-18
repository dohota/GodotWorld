import math
import pygame
from component import *
class RenderSystem:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera

    def update(self):
        self.screen.fill((30, 30, 30)) # clear
        #     # --- 视锥剔除边界 ---
    #     padding = CONFIG.HEX_SIZE * 2 * camera.zoom
    #     viewBounds = {
    #         "left": -padding,
    #         "top": -padding,
    #         "right": self.screen.get_width() + padding,
    #         "bottom": self.screen.get_height() + padding
    #     }
        entities = self.world.query(WorldPositionComponent, RenderComponent)
        ui = self.world.query(ScreenPositionComponent, RenderComponent)
        thing = entities + ui
        # layer 排序
        thing.sort(key=lambda e: self.world.get_component(e, RenderComponent).layer)
        for eid in thing:
            pos = self.world.get_component(eid, WorldPositionComponent)
            ui_pos = self.world.get_component(eid, ScreenPositionComponent)
            ren = self.world.get_component(eid, RenderComponent)
            if not ren.visible:
                continue
            if pos:
                x, y = self.world_to_screen(pos)
                self.draw(ren, x, y)
            if ui_pos:
                self.draw(ren, ui_pos.x, ui_pos.y)
        pygame.display.flip()

    def draw(self, r, x, y):
        if r.name == "unit":
            pygame.draw.rect(self.screen, (0, 0, 255), (50, 100, 200, 80))
        elif r.name == "hex":
            pass
        elif r.name == "map": # 地图作为一个整体实体，挂一个 TileMapComponent
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
        elif r.name == "ui":
            pygame.draw.rect(self.screen, (0, 0, 255), (50, 100, 200, 80))
        else:
            pass

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
        teamColor = COLORS.P1 if unit.owner == 1 else COLORS.P2
        radius = HEX_SIZE * 0.6 * zoom
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
    # def update(self, game, camera):
    #     self.clear()
    #     # --- 视锥剔除边界 ---
    #     padding = CONFIG.HEX_SIZE * 2 * camera.zoom
    #     viewBounds = {
    #         "left": -padding,
    #         "top": -padding,
    #         "right": self.screen.get_width() + padding,
    #         "bottom": self.screen.get_height() + padding
    #     }
    #     # --- 缓存缩放后的尺寸 ---
    #     hexRadius = (CONFIG.HEX_SIZE - 2) * camera.zoom
    #     selectRadius = (CONFIG.HEX_SIZE + 2) * camera.zoom
    
    #     # --- 绘制地图 ---
    #     for tile in game.map:
    #         worldPos = HexMath.hexToWorld(tile.q, tile.r)
    #         screenPos = camera.worldToScreen(worldPos["x"], worldPos["y"])
    #         # Culling
    #         if (screenPos["x"] < viewBounds["left"] or
    #             screenPos["x"] > viewBounds["right"] or
    #             screenPos["y"] < viewBounds["top"] or
    #             screenPos["y"] > viewBounds["bottom"]):
    #             continue
    #         renderedCount += 1
    #         color = CONFIG.COLORS.TILE
    #         if any(m.q == tile.q and m.r == tile.r for m in game.validMoves):
    #             color = CONFIG.COLORS.MOVE_HINT
    #         self.drawHexagon(
    #             screenPos["x"],
    #             screenPos["y"],
    #             hexRadius,
    #             color,
    #             CONFIG.COLORS.TILE_STROKE
    #         )
    #     # --- 绘制选中框 ---
    #     if game.selectedUnit:
    #         wPos = HexMath.hexToWorld(
    #             game.selectedUnit.q,
    #             game.selectedUnit.r
    #         )
    #         sPos = camera.worldToScreen(wPos["x"], wPos["y"])
    #         if viewBounds["left"] < sPos["x"] < viewBounds["right"]:
    #             self.drawHexagon(
    #                 sPos["x"],
    #                 sPos["y"],
    #                 selectRadius,
    #                 CONFIG.COLORS.HIGHLIGHT,
    #                 "gold",
    #                 2
    #             )
    #     # --- 绘制单位 ---
    #     for unit in game.units:
    #         wPos = HexMath.hexToWorld(unit.q, unit.r)
    #         sPos = camera.worldToScreen(wPos["x"], wPos["y"])

    #         if (sPos["x"] < viewBounds["left"] or
    #             sPos["x"] > viewBounds["right"] or
    #             sPos["y"] < viewBounds["top"] or
    #             sPos["y"] > viewBounds["bottom"]):
    #             continue

    #         self.drawUnit(
    #             sPos["x"],
    #             sPos["y"],
    #             unit,
    #             camera.zoom
    #         )
    def resize(self, w, h):
        self.width = w
        self.height = h
    
    #世界坐标 -> 屏幕坐标
    def worldToScreen(self, worldX, worldY):
        return {
            "x": (worldX - self.x) * self.zoom + self.width / 2,
            "y": (worldY - self.y) * self.zoom + self.height / 2
        }

    # 屏幕坐标 -> Hex网格坐标 (加入 zoom 除法)
    def screenToHex(self, screenX, screenY, hex_size):
        # 逆运算：先减去中心，除以缩放，再加上摄像机位置
        worldX = (screenX - self.width / 2) / self.zoom + self.x
        worldY = (screenY - self.height / 2) / self.zoom + self.y
        q = (2 / 3 * worldX) / hex_size
        r = (-1 / 3 * worldX + math.sqrt(3) / 3 * worldY) / hex_size
        return {
            "x": hex_size * (3/2 * q),
            "y": hex_size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
        }

    # 移动摄像机
    def pan(self, dx, dy):
        # 拖拽时，移动速度应该随缩放变化
        # 如果放得很大，拖拽应该变慢，否则会一下飞很远
        self.x -= dx / self.zoom
        self.y -= dy / self.zoom

    # 处理缩放
    def handleZoom(self, delta, mouseX, mouseY):
        print(f"[Zoom] 滚轮输入 delta: {delta}, 当前 Zoom: {self.zoom}")

        # 1. 计算缩放因子 (Scale Factor)
        direction = math.copysign(1, delta) if delta != 0 else 0
        if direction == 0:
            return

        factor = 0.1  # 每次滚动的缩放比例 (10%)

        if delta > 0:
            scaleChange = 1 - factor  # 0.9
        else:
            scaleChange = 1 + factor  # 1.1

        newZoom = self.zoom * scaleChange

        # 2. 限制缩放范围
        clampedZoom = min(max(newZoom, self.minZoom), self.maxZoom)

        print(f"[Zoom] 计算后 newZoom: {newZoom}")

        # 3. 计算以鼠标为中心的缩放
        # 缩放前：鼠标在世界的位置
        worldMouseX = (mouseX - self.width / 2) / self.zoom + self.x
        worldMouseY = (mouseY - self.height / 2) / self.zoom + self.y

        # 应用新缩放
        self.zoom = clampedZoom

        # 缩放后：反推摄像机应该在哪里
        self.x = worldMouseX - (mouseX - self.width / 2) / self.zoom
        self.y = worldMouseY - (mouseY - self.height / 2) / self.zoom
