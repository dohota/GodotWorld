class Entity:
    def __init__(self):
        self.entities = set()
        self.components = {}
        self.nextId = 0
        self.systems = []

    def createEntity(self):
        eid = self.nextId
        self.nextId += 1
        self.entities.add(eid)
        return eid

    def destroyEntity(self, eid):
        self.entities.discard(eid)
        for store in self.components.values():
            store.pop(eid, None)

    def addComponent(self, eid, comp_cls, data):
        store = self.components.setdefault(comp_cls, {})
        store[eid] = comp_cls(data)

    def query(self, *comp_classes):
        if not comp_classes:
            return []

        stores = [self.components.get(c, {}) for c in comp_classes]
        base = min(stores, key=len)

        return [
            eid for eid in base
            if all(eid in s for s in stores)
        ]
    
class UnitFactory:
    def __init__(self, world):
        self.world = world

    def create_villager(self, q, r, owner):
        eid = self.world.createEntity()
        self.world.add_component(eid, PositionComponent, {"q": q, "r": r})
        self.world.add_component(eid, CombatComponent, {"hp": 5, "owner": owner})
        self.world.add_component(eid, RenderComponent, {"sprite": "villager"})
        return eid
    
# 地图作为一个整体实体，挂一个 TileMapComponent
class MapFactory:
    def __init__(self):
        pass
