from LogicLayer.Factory.CreateSimulating import ICreateSimulator 
from LogicLayer.Factory.Simulating.BandChoiceSimulating import BandChoiceSimulating

class CreateBandChoiceSimulator(ICreateSimulator):
    def create_simulator(self, image_ms):
        """
        Create a simulator for band choice.

        Args:
            image_ms: An ImageMS object representing the multispectral image.

        Returns:
            An instance of BandChoiceSimulating.
        """
        return BandChoiceSimulating(image_ms)
