from component import *
class MoveSystem: # 检测坐标是否合规， 检测是否能移动到指定位置， 以及移动和静止时候与地形的交互
    def __init__(self, world):
        self.world = world

class CombatSystem: # 战斗，死亡，受伤，状态（状态机）
    def __init__(self, world):
        self.world = world

class MapSystem: # 处理地图，地形数据，比例尺，以及与实体的交互
    def __init__(self, world):
        self.map = world.query(TileMapComponent)
        self.initMap()

    def initMap(self):
        for q in range(-self.map.radius, self.map.radius + 1):
            r1 = max(-self.map.radius, -q - self.map.radius)
            r2 = min(self.map.radius, -q + self.map.radius)
            for r in range(r1, r2 + 1):
                key = (q, r)
                self.map[key] = {"q": q, "r": r}
