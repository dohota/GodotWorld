class Entity:
    def __init__(self, world):
        self.world = world

    def create_unit(self, q, r, color):
        eid = self.world.create_entity()
        self.world.add_component(eid, Position(q, r))
        self.world.add_component(eid, Renderable(color))
        self.world.add_component(eid, Combat(10, 3, 4))
        return eid
    
    # 地图作为一个整体实体，挂一个 TileMapComponent
    def create_map(self, q, r, color):
        eid = self.world.create_entity()
        self.world.add_component(eid, Position(q, r))
        self.world.add_component(eid, Renderable(color))
        return eid
    
    def create_ui(self, x, y, color):
        eid = self.world.create_entity()
        self.world.add_component(eid, Position(x, y))
        self.world.add_component(eid, Renderable(color))
        return eid
    