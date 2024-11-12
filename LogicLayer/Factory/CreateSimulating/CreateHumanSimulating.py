from LogicLayer.Factory.CreateSimulating import ICreateSimulator
from LogicLayer.Factory.Simulating.HumanSimulating import HumanSimulating

class CreateHumanSimulator(ICreateSimulator):
    def create_simulator(self, image_ms):
        """
        Create a simulator for human vision.

        Args:
            image_ms: An ImageMS object representing the multispectral image.

        Returns:
            An instance of HumanSimulating.
        """
        return HumanSimulating(image_ms)