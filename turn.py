from dataclasses import dataclass
# 存“每一步做了什么“
@dataclass (slots=True)
class Action:
    entity: int
    from_q: int
    from_r: int
    to_q: int
    to_r: int
# 树状历史结构 的一个节点 
class TurnNode:
    def __init__(self, action=None, parent=None):
        self.action = action
        self.parent = parent
        self.children = []

class TurnSystem:
    def __init__(self, world):
        self.world = world
        self.root = TurnNode()
        self.current_node = self.root
        self.current_player = 1
    # 某玩家结束某一回合
    def commit_action(self, action):
        node = TurnNode(action, parent=self.current_node)
        self.current_node.children.append(node)
        self.apply(action)
        self.current_node = node
        self.advance_turn()
    # 回退
    def undo(self):
        if self.current_node.parent is None:
            return
        self.undo_action(self.current_node.action)
        self.current_node = self.current_node.parent
        self.rewind_turn()
    # 分枝跳转
    # def goto(self, node):
    #     # 1. 回到最近公共祖先
    #     lca = find_lca(self.current_node, node)
    #     while self.current_node != lca:
    #         self.undo()
    #     # 2. 重做到目标节点
    #     path = build_path(lca, node)
    #     for n in path:
    #         self.apply(n.action)
    #         self.current_node = n

    # def apply(self, action):
    #     pos = self.world.get_component(action.entity, Position)
    #     pos.q = action.to_q
    #     pos.r = action.to_r

    # def undo_action(self, action):
    #     pos = self.world.get_component(action.entity, Position)
    #     pos.q = action.from_q
    #     pos.r = action.from_r
    
    # 保存整个游戏树
    # 或者对关键节点进行快照
    def save_game(self):
        pass
