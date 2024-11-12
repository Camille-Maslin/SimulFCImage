from abc import ABC, abstractmethod
from LogicLayer.Factory.Simulating import SimulatingMethod 
from LogicLayer import ImageMS

class ICreateSimulator(ABC):
    """
    Interface to create simulation methods.
    """

    @abstractmethod
    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = ()) -> SimulatingMethod:
        """
        Abstract method to create a simulator.
        Args : 
            image_ms (ImageMS) : ImageMS class object to simulate. 
            bands_number (tuple) : a tuple of integer only used for the bands number for the BandChoiceSimulation 
        Returns:
            An object of type SimulatingMethod.
        """
        pass
