import numpy as np
from math import cos, sin, radians

class Camera:
    def __init__(self, position, aspect_ratio):
        self.position = np.array(position, dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.yaw = -90.0
        self.pitch = 0.0
        self.aspect_ratio = aspect_ratio
        self.speed = 0.1
        self.sensitivity = 0.1

    # def get_view_matrix(self):
    #     # LookAt Matrix implementation
    #     z = -self.front  # Forward is -Z in OpenGL usually
    #     x = np.cross(self.up, z)
    #     x = x / np.linalg.norm(x)
    #     y = np.cross(z, x)
        
    #     # Create 4x4 View Matrix
    #     view = np.identity(4, dtype=np.float32)
    #     view[0, :3] = x
    #     view[1, :3] = y
    #     view[2, :3] = z
    #     view[:3, 3] = -np.dot(np.array([x, y, z]), self.position)
    #     return view.T # OpenGL expects column-major
    # core/camera.py 里的 get_view_matrix
    def get_view_matrix(self):
        z = -self.front
        x = np.cross(self.up, z)
        x = x / (np.linalg.norm(x) + 1e-9)
        y = np.cross(z, x)
        y = y / (np.linalg.norm(y) + 1e-9)

        view = np.identity(4, dtype=np.float32)
        view[0, :3] = x
        view[1, :3] = y
        view[2, :3] = z
        view[0, 3] = -np.dot(x, self.position)
        view[1, 3] = -np.dot(y, self.position)
        view[2, 3] = -np.dot(z, self.position)
        return view.T # 转置以匹配 OpenGL 的列主序

    def get_projection_matrix(self):
        fov = 45.0
        near = 0.1
        far = 100.0
        f = 1.0 / np.tan(radians(fov) / 2)
        
        proj = np.zeros((4, 4), dtype=np.float32)
        proj[0, 0] = f / self.aspect_ratio
        proj[1, 1] = f
        proj[2, 2] = (far + near) / (near - far)
        proj[2, 3] = -1.0
        proj[3, 2] = (2 * far * near) / (near - far)
        return proj # No transpose needed for this layout logic usually, but let's see

    def process_mouse(self, xoffset, yoffset):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0: self.pitch = 89.0
        if self.pitch < -89.0: self.pitch = -89.0

        front = np.array([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)

    def process_keyboard(self, keys):
        # 简单的 WSAD 移动
        right = np.cross(self.front, self.up)
        right = right / np.linalg.norm(right)
        
        # 这里的 119 是 pygame.K_w 的值，为了解耦暂写死或传入 map
        if keys['W']: self.position += self.front * self.speed
        if keys['S']: self.position -= self.front * self.speed
        if keys['A']: self.position -= right * self.speed
        if keys['D']: self.position += right * self.speed
