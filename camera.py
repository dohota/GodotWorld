import math
class CameraComponent:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.minZoom = 0.3  # 最远看多远 (缩小)
        self.maxZoom = 2.0  # 最近看多近 (放大)

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
    def screenToHex(self, screenX, screenY):
        # 逆运算：先减去中心，除以缩放，再加上摄像机位置
        worldX = (screenX - self.width / 2) / self.zoom + self.x
        worldY = (screenY - self.height / 2) / self.zoom + self.y

        q = (2 / 3 * worldX) / CONFIG.HEX_SIZE
        r = (-1 / 3 * worldX + math.sqrt(3) / 3 * worldY) / CONFIG.HEX_SIZE

        return HexMath.hexRound(q, r)

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
 