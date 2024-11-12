from abc import ABC, abstractmethod
from LogicLayer.Factory.Simulating import SimulatingMethod 

class ICreateSimulator(ABC):
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
