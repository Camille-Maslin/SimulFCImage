from LogicLayer.ICreateSimulator import SimulatorFactory
from HMI.BeeSimulating import BeeSimulating

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
