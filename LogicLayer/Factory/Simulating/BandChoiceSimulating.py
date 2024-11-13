from LogicLayer.Factory.Simulating import SimulatingMethod
from LogicLayer import ImageMS 
import numpy as np

class BandChoiceSimulating(SimulatingMethod):

    def __init__(self, image_ms : ImageMS, bands_number : tuple):
        """
        Constructor to initialize the multispectral image and related data.

        Args:
            image_ms (ImageMS) : An ImageMS object representing the multispectral image to simulate.
            bands_number (tuple) : the bands number as a tuple of Band object for the simulation.
        """
        super().__init__(image_ms)
        self.__bands = bands_number

    def simulate(self) -> np.ndarray :
        # Separating the channels of the selected band into RGB
        red_band = self.__bands[0]
        green_band = self.__bands[1]
        blue_band = self.__bands[2]

        # Normalizing the image (not obligated)
        red = (red_band - red_band.min()) / (red_band.max() - red_band.min())
        green = (green_band - green_band.min()) / (green_band.max() - green_band.min())
        blue = (blue_band - blue_band.min()) / (blue_band.max() - blue_band.min())

        sim_image = np.stack((red, green, blue), axis = 2) # Simulated image generated
        return sim_image
        
