import pygame
from pygame.locals import *
from OpenGL.GL import *

from core.shader import Shader
from core.camera import Camera
from world.world import World
import numpy as np

pygame.init()
display = (800, 600)
# --- 新增代码开始 ---
    # 强制告诉 macOS 使用 OpenGL 3.3 Core Profile
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True) # Mac 必须加这句
# --- 新增代码结束 ---
    # 开启 Double Buffer 和 OpenGL 上下文
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # 捕获鼠标并隐藏
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
# --- 【新增修复代码】开始 ---
    # macOS Core Profile 强制要求：必须有一个 VAO 被绑定，否则 Shader 验证会失败
    # 我们创建一个全局的空 VAO，一直绑着就行
global_vao = glGenVertexArrays(1)
glBindVertexArray(global_vao)
    # --- 【新增修复代码】结束 ---
# OpenGL 设置
glEnable(GL_DEPTH_TEST)   # 开启深度测试：让前面的方块遮住后面的方块
glDepthFunc(GL_LESS)      # 深度测试函数
glEnable(GL_CULL_FACE)    # 开启背面剔除：不渲染方块的内部面，提升一倍性能
glCullFace(GL_BACK)       # 剔除背面
glClearColor(0.5, 0.7, 1.0, 1.0) # 天空蓝背景
    # 初始化核心组件
shader = Shader()
# 稍微离远一点，看全景
camera = Camera([16, 32, 48], display[0]/display[1]) 
camera.yaw = -90
camera.pitch = -30
world = World()

clock = pygame.time.Clock()

running = True
while running:
        # 1. 事件处理
    dt = clock.tick(60) / 1000.0 # Delta time
        
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.rel
                camera.process_mouse(x, -y)

    keys = pygame.key.get_pressed()
    input_map = {
            'W': keys[pygame.K_w],
            'S': keys[pygame.K_s],
            'A': keys[pygame.K_a],
            'D': keys[pygame.K_d]
        }
    camera.process_keyboard(input_map)

        # 2. 逻辑更新
    world.update()
    # --- 新增调试打印 ---
    # 每 60 帧打印一次，避免刷屏
    if pygame.time.get_ticks() % 60 == 0:
        print(f"Pos: {camera.position}, Yaw: {camera.yaw}, Pitch: {camera.pitch}")
    # ------------------
        # 3. 渲染
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    shader.use()
        
        # 传递矩阵给 Shader
    proj = camera.get_projection_matrix()
    view = camera.get_view_matrix()
        
    shader.set_mat4("projection", proj)
    shader.set_mat4("view", view)
    
    world.render(shader)

    pygame.display.flip()

pygame.quit() 

# if __name__ == "__main__":
#     main()
