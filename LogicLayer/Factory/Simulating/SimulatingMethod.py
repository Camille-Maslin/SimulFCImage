from abc import ABC, abstractmethod
import numpy as np

from LogicLayer import ImageMS

class SimulateMethod(ABC):
    """
    Abstract class to define a simulation method.
    """
    def __init__(self, image_ms : ImageMS):
        """
        Constructor to initialize the multispectral image.

        Args:
            image_ms (ImageMS): An ImageMS object representing the multispectral image to simulate.
        """
        self._image_ms = image_ms
        # Coefficient based on CIE 1931 color matching functions
        self._color_balance = {
            'R': 1.0,
            'G': 1.0,
            'B': 1.0
        }

    @abstractmethod
    def simulate(self) -> np.ndarray:
        """
        Abstract method to simulate an image.

        Returns:
            The simulated image data as an ndarray.
        """
        pass
    
    @abstractmethod
    def calculate_sensitivity(self, wavelength : float) -> tuple :
        pass  