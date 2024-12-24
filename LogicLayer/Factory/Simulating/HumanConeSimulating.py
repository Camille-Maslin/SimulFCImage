from LogicLayer.Factory.Simulating.SimulatingMethod import SimulateMethod
from Storage.FileManager import FileManager

import numpy as np

class HumanConeSimulating(SimulateMethod):
    """
    A class that simulates human color vision using real spectral sensitivity data.
    This implementation uses the Stiles & Burch 2-degree cone fundamentals instead
    of Gaussian approximations for more accurate results.
    
    References:
        - Data source: http://www.cvrl.org/cones.htm
        - Stiles, W. S., & Burch, J. M. (1959). N.P.L. colour-matching investigation:
          Final report (1958). Optica Acta, 6, 1-26.
    """
    
    def __init__(self, image_ms):
        """
        Constructor for HumanConeSimulating which calls the constructor of SimulateMethod.
        Loads the real spectral sensitivity data from a CSV file.
        """
        super().__init__(image_ms)
        self.spectral_sensitivity = FileManager.open_and_load_sensitivity_data()

    def calculate_sensitivity(self, wavelength: float) -> tuple:
        """
        Calculates cone sensitivities using interpolated Stiles & Burch data.
        Uses cached interpolation function for better performance and accuracy.
        
        Args:
            wavelength (float): The wavelength in nanometers (380-780nm)
        
        Returns:
            tuple: (L, M, S) cone sensitivity values
        """
        # Use the interpolation function from _load_sensitivity_data
        sensitivities = self.spectral_sensitivity(wavelength)
        L, M, S = sensitivities
        
        return L, M, S

    def simulate(self) -> np.ndarray:
        """
        Simulates human vision using Stiles & Burch cone fundamentals,
        with normalization similar to V1 for better consistency.
        """
        # Get image dimensions from size tuple (width, height)
        width, height = self._image_ms.get_size()
        rgb_image = np.zeros((height, width, 3), dtype=np.float32)
        
        # Accumulate responses
        for band in self._image_ms.get_bands():
            wavelength = band.get_wavelength()[0]  # Get the minimum wavelength from the tuple
            band_data = band.get_shade_of_grey().astype(np.float32) / 255.0  # Normalize to [0,1]
            L, M, S = self.calculate_sensitivity(wavelength)
            
            # Accumulate responses
            rgb_image[:,:,0] += band_data * L  # L-cone
            rgb_image[:,:,1] += band_data * M  # M-cone
            rgb_image[:,:,2] += band_data * S  # S-cone
        
        # Normalize each channel independently
        for i in range(3):
            channel = rgb_image[:,:,i]
            if np.any(channel):  # Only normalize if channel has non-zero values
                min_val = np.min(channel)
                max_val = np.max(channel)
                if max_val > min_val:
                    # Normalize to [0,1]
                    rgb_image[:,:,i] = (channel - min_val) / (max_val - min_val)
        
        # Ensure all values are in [0,1] range
        rgb_image = np.clip(rgb_image, 0, 1)
        
        return rgb_image 