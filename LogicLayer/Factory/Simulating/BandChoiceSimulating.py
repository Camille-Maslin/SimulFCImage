from LogicLayer.Factory.Simulating import SimulatingMethod
from LogicLayer import ImageMS 

class BandChoiceSimulating(SimulatingMethod):

    def __init__(self, image_ms : ImageMS, bands_number : tuple):
        """
        Constructor to initialize the multispectral image and related data.

        Args:
            image_ms (ImageMS) : An ImageMS object representing the multispectral image to simulate.
            bands_number (tuple) : the bands number as a tuple of int for the simulation.
        """
        super().__init__(image_ms)
        self.__bands_number = bands_number

    def simulate(self):
        pass 
