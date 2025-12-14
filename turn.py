class TurnSystem:
    def __init__(self, world):
        self.world = world
        self.history = []  # 存储回合快照
        self.currentTurn = 0

    def save_state(self):
        snapshot = {}  # 可以存所有单位状态，或者整个世界状态
        for entity in self.world.entities:
            pos = self.world.get_component(entity, PositionComponent)
            combat = self.world.get_component(entity, CombatComponent)
            snapshot[entity] = (pos.q, pos.r, combat.hp)
        self.history.append(snapshot)

    def undo_turn(self, turn_index):
        snapshot = self.history[turn_index]
        for entity, state in snapshot.items():
            pos = self.world.get_component(entity, PositionComponent)
            combat = self.world.get_component(entity, CombatComponent)
            pos.q, pos.r, combat.hp = state
        self.currentTurn = turn_index
