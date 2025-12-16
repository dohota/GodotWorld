import pygame
from world import *
from render import *
from turn import *
from entity import *
from input import *
from system import *
class Manager:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Warchess")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 24)
        self.world = World()
        self.world.add_system(RenderSystem(self.screen))
        self.world.add_system(InputSystem(self.screen, self.camera, self.handleInput, self.toggleUI))
        self.world.add_system(TurnSystem(self.world))
        self.world.add_system(MoveSystem(self.world))
        self.world.add_system(CombatSystem(self.world))
        self.factory = EntityFactory(self.world)
        self.u1 = self.factory.create("unit",[10,10,"unit"])
        self.u2 = self.factory.create("unit",[0,0,"unit"])
        self.camera = self.factory.create("camera",[2,5])

    def initMap(self):
        for q in range(-CONFIG.MAP_RADIUS, CONFIG.MAP_RADIUS + 1):
            r1 = max(-CONFIG.MAP_RADIUS, -q - CONFIG.MAP_RADIUS)
            r2 = min(CONFIG.MAP_RADIUS, -q + CONFIG.MAP_RADIUS)
            for r in range(r1, r2 + 1):
                key = HexMath.getKey(q, r)
                self.map[key] = {"q": q, "r": r}

    def handleInput(self, hex_pos):
        key = HexMath.getKey(hex_pos.q, hex_pos.r)
        if key not in self.map:
            return
        clickedUnit = next((u for u in self.units if u.q == hex_pos.q and u.r == hex_pos.r), None)
        if clickedUnit and clickedUnit.owner == self.currentPlayer:
            self.selectedUnit = clickedUnit
            self.calculateValidMoves(clickedUnit)
        elif self.selectedUnit and not clickedUnit:
            self.tryMove(hex_pos)

    def calculateValidMoves(self, unit):
        self.validMoves = []
        for tile in self.map.values():
            dist = HexMath.getDistance(unit, tile)
            if dist <= unit.move and dist > 0:
                isOccupied = any(
                    u.q == tile["q"] and u.r == tile["r"]
                    for u in self.units
                )
                if not isOccupied:
                    self.validMoves.append(tile)

    def tryMove(self, targetHex):
        isValid = any(
            m["q"] == targetHex.q and m["r"] == targetHex.r
            for m in self.validMoves
        )

        if isValid:
            self.selectedUnit.q = targetHex.q
            self.selectedUnit.r = targetHex.r
            self.selectedUnit = None
            self.validMoves = []
            self.switchTurn()
        else:
            self.selectedUnit = None
            self.validMoves = []

    def switchTurn(self):
        self.currentPlayer = 2 if self.currentPlayer == 1 else 1

    def drawTurnText(self):
        text = "红方回合" if self.currentPlayer == 1 else "蓝方回合"
        color = CONFIG.COLORS.P1 if self.currentPlayer == 1 else CONFIG.COLORS.P2

        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (20, 20))

    def update(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.size
                    self.screen = pygame.display.set_mode(
                        (self.width, self.height),
                        pygame.RESIZABLE
                    )
                    self.camera.resize(self.width, self.height)
                self.input.handle_event(event)
            self.world.update(dt)
        pygame.quit()

if __name__ == "__main__":
    m = Manager()
    m.update()
