from LogicLayer.Factory.CreateSimulating.ICreateSimulator import SimulatorFactory
from LogicLayer.Factory.Simulating.BeeSimulating import BeeSimulating

class CreateBeeSimulator(SimulatorFactory):
    def create_simulator(self, image_ms):
        """
        Create a simulator for bee vision.

        Args:
            image_ms: An ImageMS object representing the multispectral image.

        Returns:
            An instance of BeeSimulating.
        """
        return BeeSimulating(image_ms)
