from LogicLayer.SimulatingMethod import SimulatingMethod

class DaltonianSimulating(SimulatingMethod):
    def __init__(self, image_ms):
        super().__init__(image_ms)

    def simulate(self):
        return self.image_ms  
