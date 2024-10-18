from LogicLayer.ICreateSimulator import SimulatorFactory
from LogicLayer.DaltonianSimulating import DaltonianSimulating

class CreateDaltonianSimulator(SimulatorFactory):
    def create_simulator(self, image_ms):
        """
        Create a simulator for daltonian vision.

        Args:
            image_ms: An ImageMS object representing the multispectral image.

        Returns:
            An instance of DaltonianSimulating.
        """
        return DaltonianSimulating(image_ms)
