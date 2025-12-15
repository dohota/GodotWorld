from dataclasses import dataclass
# 加上@dataclass (slots=True)，则等同于如下代码
# class Position:
#     def __init__(self, q, r):
#         self.q = q
#         self.r = r

#     def __repr__(self):
#         return f"Position(q={self.q}, r={self.r})"

#     def __eq__(self, other):
#         return self.q == other.q and self.r == other.r
@dataclass (slots=True)
class WorldPositionComponent:
    x: float
    y: float
    z: float

@dataclass(slots=True)
class ScreenPositionComponent:
    x: int
    y: int

@dataclass(slots=True)
class MapPositionComponent:
    q: int
    r: int

@dataclass(slots=True)
class RenderComponent:
    border_color: str
    fill_color: str
    size: float
    name: str    

@dataclass(slots=True)
class CombatComponent:
    def __init__(self, hp: int, attack: int, defense: int, move: int):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.move = move 
                