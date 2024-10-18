from LogicLayer.Factory.Simulating.SimulatingMethod import SimulatingMethod

class HumanSimulating(SimulatingMethod):
    def __init__(self, image_ms):
        super().__init__(image_ms)

    def simulate(self):
        return self.image_ms  
