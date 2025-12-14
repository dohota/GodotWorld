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

class Chess:
    pass