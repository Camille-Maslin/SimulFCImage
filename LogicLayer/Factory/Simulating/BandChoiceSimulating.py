from LogicLayer.Factory.Simulating.SimulatingMethod import SimulateMethod
from LogicLayer import ImageMS 
import numpy as np

class BandChoiceSimulating(SimulateMethod):

    def __init__(self, image_ms : ImageMS, bands_number : tuple):
        """
        Constructor to initialize the multispectral image and related data.

        Args:
            image_ms (ImageMS) : An ImageMS object representing the multispectral image to simulate.
            bands_number (tuple) : the bands number as a tuple of Band object for the simulation.
        """
        super().__init__(image_ms)
        self.__bands = bands_number

    def simulate(self) -> np.ndarray:
        """
        Merges three selected bands into an RGB image.
        Each band is assigned to a specific color channel (R, G or B).
        
        @returns: np.ndarray: Normalized RGB image

        Author :  Lakhdar Gibril, Camille Maslin
        """
        # Retrieving the data of each band
        red_data = self.__bands[0].get_shade_of_grey()
        green_data = self.__bands[1].get_shade_of_grey()
        blue_data = self.__bands[2].get_shade_of_grey()
        
        # Normalization of the data for each channel (0-1)
        red_normalized = (red_data - np.min(red_data)) / (np.max(red_data) - np.min(red_data))
        green_normalized = (green_data - np.min(green_data)) / (np.max(green_data) - np.min(green_data))
        blue_normalized = (blue_data - np.min(blue_data)) / (np.max(blue_data) - np.min(blue_data))
        
        # Creating the RGB image by stacking the three channels
        rgb_image = np.dstack((red_normalized, green_normalized, blue_normalized))
        
        return rgb_image