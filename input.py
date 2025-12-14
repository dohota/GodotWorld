import pygame
# 输入系统: 处理鼠标交互，区分拖拽和点击
class InputSystem:
    def __init__(self, screen, camera, onClickCallback, onKeyCallback):
        self.screen = screen
        self.camera = camera
        self.onClick = onClickCallback
        self.onKey = onKeyCallback

        self.state = {
            "isDragging": False,
            "hasMoved": False,
            "startX": 0,
            "startY": 0
        }

    # 等价于 JS 的事件回调系统
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                self.onMouseDown(event)

        elif event.type == pygame.MOUSEMOTION:
            self.onMouseMove(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.onMouseUp(event)

        elif event.type == pygame.MOUSEWHEEL:
            self.onWheel(event)

        elif event.type == pygame.KEYDOWN:
            self.onKeyDown(event)

    def onMouseDown(self, event):
        self.state["isDragging"] = True
        self.state["hasMoved"] = False
        self.state["startX"] = event.pos[0]
        self.state["startY"] = event.pos[1]
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    # 注意：camera.pan 内部已经除以 zoom，这里不需要改
    def onMouseMove(self, event):
        if not self.state["isDragging"]:
            return

        dx = event.pos[0] - self.state["startX"]
        dy = event.pos[1] - self.state["startY"]

        # 检测是否达到拖拽阈值,拖拽阈值=5
        if abs(dx) > 5 or abs(dy) > 5:
            self.state["hasMoved"] = True

        # 移动摄像机
        self.camera.pan(dx, dy)

        # 更新起始点，避免累积误差
        self.state["startX"] = event.pos[0]
        self.state["startY"] = event.pos[1]

    def onMouseUp(self, event):
        self.state["isDragging"] = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if not self.state["hasMoved"]:
            # 触发点击回调
            hex_pos = self.camera.screenToHex(event.pos[0], event.pos[1])
            self.onClick(hex_pos)

    def onMouseLeave(self):
        self.state["isDragging"] = False

    def onWheel(self, event):
        # Pygame 中 wheel 没有默认滚动，不需要 preventDefault
        # event.y: 上滚 = 1, 下滚 = -1
        delta = -event.y * 100  # 等价于 JS 中常见的 deltaY
        mouseX, mouseY = pygame.mouse.get_pos()
        self.camera.handleZoom(delta, mouseX, mouseY)

    def onKeyDown(self, event):
        if event.key == pygame.K_p:
            if self.onKey:
                self.onKey()
