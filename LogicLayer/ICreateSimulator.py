from abc import ABC, abstractmethod
from LogicLayer.SimulatingMethod import SimulatingMethod 

class SimulatorFactory(ABC):
    """
    Interface to create simulation methods.
    """

    @abstractmethod
    def create_simulator(self) -> SimulatingMethod:
        """
        Abstract method to create a simulator.

        Returns:
            An object of type SimulatingMethod.
        """
        pass
