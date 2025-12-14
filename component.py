class WorldPositionComponent:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

class ScreenPositionComponent:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class MapPositionComponent:
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r

class RenderComponent:
    def __init__(self, border_color: str, fill_color: str, size: float, name: str = ""):
        self.border_color = border_color
        self.fill_color = fill_color    
        self.size = size     
        self.name = name      

class CombatComponent:
    def __init__(self, hp: int, attack: int, defense: int, move: int):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.move = move 
                