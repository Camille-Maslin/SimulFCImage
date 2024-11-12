from abc import ABC, abstractmethod
from LogicLayer import ImageMS

class SimulateMethod(ABC):
    """
    Abstract class to define a simulation method.
    """

    def __init__(self, image_ms : ImageMS):
        """
        Constructor to initialize the multispectral image.

        Args:
            image_ms: An ImageMS object representing the multispectral image to simulate.
        """
        self._image_ms = image_ms

    @abstractmethod
    def simulate(self):
        """
        Abstract method to simulate an image.

        Returns:
            The simulated image data.
        """
        pass
