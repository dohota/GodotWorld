from dataclasses import dataclass
# 加上@dataclass (slots=True)，则等同于如下代码
# class Position:
#     def __init__(self, q:int, r:int):
#         self.q = q
#         self.r = r

#     def __repr__(self):
#         return f"Position(q={self.q}, r={self.r})"

#     def __eq__(self, other):
#         return self.q == other.q and self.r == other.r
@dataclass (slots=True) 
class WorldPositionComponent: # render system会把 实际位置转化为 在屏幕上显示的位置
    x: float
    y: float
    z: float

@dataclass(slots=True)
class ScreenPositionComponent: # 只有ui没有实际位置，只有固定的在屏幕上的位置
    x: int
    y: int

@dataclass(slots=True)
class RenderComponent:
    name: str 
    layer: int = 1
    visible: bool = True
    border_color: str = ""
    fill_color: str = ""
    size: float = 2

@dataclass(slots=True)
class CombatComponent:
    hp: int
    attack: int
    defence: int
    move: int

class CameraComponent:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.minZoom = 0.3  # 最远看多远 (缩小)
        self.maxZoom = 2.0  # 最近看多近 (放大)
 
@dataclass(slots=True)
class TileMapComponent:
    q: int
    r: int
    size: int = 30
    radius: int = 40
    type: str = ""# 应该为str数组
    name: str = "hex" # 六角格地图

@dataclass(slots=True)
class StepComponent: # 该实体踩在什么样的地面上，环境是什么
    type: str
