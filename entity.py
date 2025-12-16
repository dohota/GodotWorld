from component import *

class EntityFactory:
    def __init__(self, world):
        self.world = world

    def create(self, name, a):
        eid = self.world.create_entity()
        if name == "unit":
            self.world.add_component(eid, WorldPositionComponent(a[0], a[1]))
            self.world.add_component(eid, RenderComponent(name))
            self.world.add_component(eid, CombatComponent(10, 3, 4))
        elif name == "hex":
            pass
        elif name == "map": # 地图作为一个整体实体，挂一个 TileMapComponent
            self.world.add_component(eid, TileMapComponent(a[0], a[1]))
            self.world.add_component(eid, RenderComponent(name))
        elif name == "camera":
            self.world.add_component(eid, CameraComponent(a[0], a[1]))
        elif name == "ui":
            self.world.add_component(eid, ScreenPositionComponent(a[0], a[1]))
            self.world.add_component(eid, RenderComponent(name))
        else:
            pass
        return eid
    