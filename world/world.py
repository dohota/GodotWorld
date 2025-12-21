from .chunk import Chunk

class World:
    def __init__(self):
        self.chunks = {}
        # 铺一个 4x4 的大平面，总共 64x64 个方块
        for x in range(-2, 2):
            for z in range(-2, 2):
                self.chunks[(x, 0, z)] = Chunk(self, (x, 0, z))

    def update(self):
        for chunk in self.chunks.values():
            chunk.update()

    def render(self, shader):
        for chunk in self.chunks.values():
            chunk.render(shader)
