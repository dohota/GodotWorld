import numpy as np
from OpenGL.GL import *
import ctypes

class Chunk:
    def __init__(self, world, position):
        self.world = world
        self.position = position # (x, y, z) tuple
        self.size = 16
        # 16x16x16 的方块数据，0=空，1=方块
        #self.blocks = np.random.choice([0, 1], size=(self.size, self.size, self.size), p=[0.2, 0.8])
        # 修改为全满方块，方便测试
        #self.blocks = np.ones((self.size, self.size, self.size), dtype=np.int32)
        # 生成一个 16x4x16 的实心基岩层
        self.blocks = np.zeros((self.size, self.size, self.size), dtype=np.int32)
        self.blocks[:, 0:4, :] = 1 # 只有底部4层有方块
        self.vao = None
        self.vbo = None
        self.vertex_count = 0
        self.is_dirty = True # 标记是否需要重新生成网格

    def generate_mesh(self):
        vertices = []
        
        # 定义立方体的6个面法向量和顶点偏移
        # 格式: x, y, z, r, g, b
        # 简单起见，我们根据位置给它上色
        
        # 优化：不遍历所有方块，而是根据 self.blocks 快速判断
        # 这里用 Python 循环演示逻辑，进阶可以用 Numpy 掩码加速
        
        cx, cy, cz = self.position
        
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if self.blocks[x][y][z] == 0:
                        continue
                    
                    # 绝对坐标
                    abs_x, abs_y, abs_z = cx * self.size + x, cy * self.size + y, cz * self.size + z
                    
                    # 检查6个邻居，如果是空气(0)或者是边界，就画那个面
                    # 简化的 Face Culling
                    
                    # Top (Y+)
                    if y == self.size - 1 or self.blocks[x][y+1][z] == 0:
                        self.add_face(vertices, abs_x, abs_y, abs_z, 'top')
                    # Bottom (Y-)
                    if y == 0 or self.blocks[x][y-1][z] == 0:
                        self.add_face(vertices, abs_x, abs_y, abs_z, 'bottom')
                    # ... 其他4个面略，为了代码简短演示原理 ...
                    # Front (Z+)
                    if z == self.size - 1 or self.blocks[x][y][z+1] == 0:
                         self.add_face(vertices, abs_x, abs_y, abs_z, 'front')
                    # Back (Z-)
                    if z == 0 or self.blocks[x][y][z-1] == 0:
                         self.add_face(vertices, abs_x, abs_y, abs_z, 'back')
                    # Right (X+)
                    if x == self.size - 1 or self.blocks[x+1][y][z] == 0:
                         self.add_face(vertices, abs_x, abs_y, abs_z, 'right')
                    # Left (X-)
                    if x == 0 or self.blocks[x-1][y][z] == 0:
                         self.add_face(vertices, abs_x, abs_y, abs_z, 'left')

        return np.array(vertices, dtype=np.float32)

    def add_face(self, vertices, x, y, z, face):
        # 这里的颜色根据高度或面来变化，增加层次感
        colors = {
            'top': [0.1, 0.8, 0.1],    # 绿色草地
            'bottom': [0.5, 0.3, 0.1], # 泥土
            'left': [0.6, 0.6, 0.6],   # 灰色侧面
            'right': [0.5, 0.5, 0.5],
            'front': [0.7, 0.7, 0.7],
            'back': [0.4, 0.4, 0.4],
        }
        c = colors.get(face, [1, 1, 1])

        # 顶点顺序必须是逆时针(CCW)才是正面
        data = []
        if face == 'top':
            data = [
                x, y+1, z,   *c,   x+1, y+1, z, *c,   x, y+1, z+1, *c,
                x, y+1, z+1, *c,   x+1, y+1, z, *c,   x+1, y+1, z+1, *c
            ]
        elif face == 'bottom':
            data = [
                x, y, z,   *c,     x, y, z+1, *c,     x+1, y, z, *c,
                x+1, y, z, *c,     x, y, z+1, *c,     x+1, y, z+1, *c
            ]
        elif face == 'front': # Z+
            data = [
                x, y, z+1, *c,     x+1, y, z+1, *c,   x, y+1, z+1, *c,
                x, y+1, z+1, *c,   x+1, y, z+1, *c,   x+1, y+1, z+1, *c
            ]
        elif face == 'back': # Z-
            data = [
                x, y, z, *c,       x, y+1, z, *c,     x+1, y, z, *c,
                x+1, y, z, *c,     x, y+1, z, *c,     x+1, y+1, z, *c
            ]
        elif face == 'left': # X-
            data = [
                x, y, z, *c,       x, y, z+1, *c,     x, y+1, z, *c,
                x, y+1, z, *c,     x, y, z+1, *c,     x, y+1, z+1, *c
            ]
        elif face == 'right': # X+
            data = [
                x+1, y, z, *c,     x+1, y+1, z, *c,   x+1, y, z+1, *c,
                x+1, y, z+1, *c,   x+1, y+1, z, *c,   x+1, y+1, z+1, *c
            ]
        vertices.extend(data)
    # def add_face(self, vertices, x, y, z, face):
    #     # 简单的颜色区分
    #     c = [0.5, 0.5, 0.5]
    #     if face == 'top': c = [0.2, 0.8, 0.2] # Green
    #     elif face == 'bottom': c = [0.5, 0.3, 0.1] # Dirt
    #     elif face == 'front': c = [0.6, 0.6, 0.6]
        
    #     # 一个面由两个三角形组成（6个顶点）
    #     # 这里仅写出 Top 面作为示例，其他面同理需要补全几何数据
    #     if face == 'top':
    #         # p1, c1, p2, c2 ...
    #         v = [
    #             x, y+1, z,   *c,
    #             x+1, y+1, z, *c,
    #             x, y+1, z+1, *c,
                
    #             x, y+1, z+1, *c,
    #             x+1, y+1, z, *c,
    #             x+1, y+1, z+1, *c
    #         ]
    #         vertices.extend(v)
    #     # ！！！注意：为了运行完整，你需要补全 bottom, left, right, front, back 的坐标！！！
    #     # 为了演示代码简洁，这里用简略逻辑代替：
    #     else:
    #          # 通用伪代码：根据face类型添加对应的6个顶点
    #          # 实际开发需手写这部分繁琐的坐标
    #          self.add_cube_face_geometry(vertices, x, y, z, face, c)

    def add_cube_face_geometry(self, vertices, x, y, z, face, c):
        # 这是一个辅助函数，用来快速生成其他面的几何体
        # 偏移量字典
        offsets = {
            'front':  [(0,0,1), (1,0,1), (0,1,1), (0,1,1), (1,0,1), (1,1,1)],
            'back':   [(1,0,0), (0,0,0), (1,1,0), (1,1,0), (0,0,0), (0,1,0)],
            'left':   [(0,0,0), (0,0,1), (0,1,0), (0,1,0), (0,0,1), (0,1,1)],
            'right':  [(1,0,1), (1,0,0), (1,1,1), (1,1,1), (1,0,0), (1,1,0)],
            'bottom': [(0,0,1), (1,0,1), (0,0,0), (0,0,0), (1,0,1), (1,0,0)],
        }
        if face in offsets:
            for dx, dy, dz in offsets[face]:
                vertices.extend([x+dx, y+dy, z+dz, *c])

    def update(self):
        if self.is_dirty:
            data = self.generate_mesh()
            self.vertex_count = len(data) // 6 # 每个顶点6个float (3pos + 3color)
            
            if self.vao is None:
                self.vao = glGenVertexArrays(1)
                self.vbo = glGenBuffers(1)

            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

            # 解析顶点数据: 0=Pos(3f), 1=Color(3f)
            # stride = 6 * 4 bytes (float32)
            stride = 6 * 4
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
            glEnableVertexAttribArray(1)
            
            self.is_dirty = False

    def render(self, shader):
        if self.vertex_count > 0:
            shader.set_mat4("model", np.identity(4, dtype=np.float32))
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)