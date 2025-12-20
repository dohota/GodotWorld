import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
# ---- 世界配置 ----
world_size = (16, 8, 16)  # x, y, z
world = np.zeros(world_size, dtype=int)
world[:, :4, :] = 1  # 地面层填充
# ---- 方块渲染 ----
def draw_cube(x, y, z):
    vertices = [
        (x, y, z),
        (x+1, y, z),
        (x+1, y+1, z),
        (x, y+1, z),
        (x, y, z+1),
        (x+1, y, z+1),
        (x+1, y+1, z+1),
        (x, y+1, z+1)
    ]
    edges = (
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    )
    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(vertices[vertex])
    # glEnd()
    glBegin(GL_LINES)
    glColor3f(0.8, 0.8, 0.8)  # 浅灰色
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

class Camera:
    def __init__(self, pos, yaw=0, pitch=0):
        self.pos = np.array(pos, dtype=float)
        self.yaw = yaw
        self.pitch = pitch
        self.speed = 0.2
        self.mouse_sensitivity = 0.2

    def move(self, keys):
        direction = np.array([0.0, 0.0, 0.0])
        rad_yaw = math.radians(self.yaw)
        forward = np.array([math.sin(rad_yaw), 0, -math.cos(rad_yaw)])
        right = np.array([math.cos(rad_yaw), 0, math.sin(rad_yaw)])

        if keys[pygame.K_w]:
            direction += forward
        if keys[pygame.K_s]:
            direction -= forward
        if keys[pygame.K_a]:
            direction -= right
        if keys[pygame.K_d]:
            direction += right

        # 规范化方向向量
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)

        # 碰撞检测：简单阻止进入方块
        new_pos = self.pos + direction * self.speed
        x, y, z = map(int, new_pos)
        if 0 <= x < world_size[0] and 0 <= y < world_size[1] and 0 <= z < world_size[2]:
            if world[x, int(self.pos[1]), z] == 0:  # 只有空地可以移动
                self.pos = new_pos

    def apply(self):
        glRotatef(-self.pitch, 1, 0, 0)
        glRotatef(-self.yaw, 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])
# ---- 初始化 Pygame + OpenGL ----
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(70, (display[0]/display[1]), 0.1, 100.0)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL) # unknown
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

camera = Camera(pos=(8,6,20), yaw=180, pitch=0)
clock = pygame.time.Clock()
while True:
    dt = clock.tick(60)
    glClearColor(0.5, 0.7, 1.0, 1.0)  # 天空蓝
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
    keys = pygame.key.get_pressed()
    camera.move(keys)
    # 鼠标旋转
    mx, my = pygame.mouse.get_rel()
    camera.yaw += mx * camera.mouse_sensitivity
    camera.pitch += my * camera.mouse_sensitivity
    camera.pitch = max(-90, min(90, camera.pitch))

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.apply()
    # 绘制方块世界
    for x in range(world_size[0]):
        for y in range(world_size[1]):
            for z in range(world_size[2]):
                if world[x,y,z] != 0:
                    draw_cube(x, y, z)

    pygame.display.flip()

# class Manager:
#     def __init__(self):
#         pygame.init()
#         info = pygame.display.Info()
#         self.width = info.current_w
#         self.height = info.current_h
#         self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
#         pygame.display.set_caption("Warchess")
#         self.clock = pygame.time.Clock()
#         self.running = True
#         self.font = pygame.font.SysFont("Arial", 24)

#     def update(self):
#         while self.running:
#             dt = self.clock.tick(60) / 1000
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                 elif event.type == pygame.VIDEORESIZE:
#                     self.width, self.height = event.size
#                     self.screen = pygame.display.set_mode(
#                         (self.width, self.height),
#                         pygame.RESIZABLE
#                     )
#             #         self.camera.resize(self.width, self.height)
#             #     self.input.handle_event(event)
#             # self.world.update(dt)
#         pygame.quit()

# if __name__ == "__main__":
#     m = Manager()
#     m.update()
