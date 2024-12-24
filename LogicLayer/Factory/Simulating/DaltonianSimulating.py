from LogicLayer.Factory.Simulating.SimulatingMethod import SimulateMethod
import numpy as np
from LogicLayer.ImageMS import ImageMS

class DaltonianSimulating(SimulateMethod):
    """
    Simulates color vision deficiencies (color blindness) based on scientific models.
    
    Implements various types of color vision deficiencies:
    - Dichromatic vision (Deuteranopia, Protanopia, Tritanopia)
    - Anomalous trichromatic vision (Deuteranomaly, Protanomaly, Tritanomaly)
    - Complete color blindness (Achromatopsia)
    
    Based on research from:
    - Brettel et al. (1997) for dichromatic vision
    - Machado et al. (2009) for anomalous trichromatic vision
    - Carroll et al. (2004) for severity ratios
    - Kraft et al. (1993) for rod spectral sensitivity
    """

    def __init__(self, image_ms: ImageMS, daltonian_type: str = "Deuteranopia"):
        """
        Initialize the color vision deficiency simulator.
        
        Args:
            image_ms (ImageMS): Multispectral image to simulate
            daltonian_type (str): Type of color vision deficiency to simulate
                                 Default is "Deuteranopia" (most common type)
        """
        super().__init__(image_ms)
        self.__daltonian_type = daltonian_type

    def calculate_sensitivity(self, wavelength: float) -> tuple:
        """
        Calculate cone sensitivities for different types of color vision deficiencies.
        
        Uses Stockman & Sharpe (2000) cone fundamentals as baseline sensitivities,
        then modifies them according to the type of color vision deficiency.
        
        Args:
            wavelength (float): Wavelength in nanometers
            
        Returns:
            tuple: Modified cone sensitivities (S, M, L) normalized to sum to 1
        """
        # Base sensitivities (Stockman & Sharpe 2000 peaks)
        S = np.exp(-((wavelength - 441.8)**2) / (2 * 28**2)) * self._color_balance['B']
        M = np.exp(-((wavelength - 541.2)**2) / (2 * 38**2)) * self._color_balance['G']
        L = np.exp(-((wavelength - 566.8)**2) / (2 * 48**2)) * self._color_balance['R']

        severity = 0.75  # Standard severity for anomalous trichromacy (75%)

        # Apply modifications based on color vision deficiency type
        if self.__daltonian_type == "Deuteranopia":
            # Complete absence of M cones
            M = 0.95 * L + 0.05 * S if wavelength > 545 else 0.05 * L + 0.95 * S

        elif self.__daltonian_type == "Protanopia":
            # Complete absence of L cones
            L = 0.95 * M + 0.05 * S if wavelength > 545 else 0.05 * M + 0.95 * S

        elif self.__daltonian_type == "Tritanopia":
            # Complete absence of S cones
            S = 0.5 * M + 0.5 * L

        elif self.__daltonian_type == "Deuteranomaly":
            # Partial M cone dysfunction
            M = (1 - severity) * M + severity * L

        elif self.__daltonian_type == "Protanomaly":
            # Partial L cone dysfunction
            L = (1 - severity) * L + severity * M

        elif self.__daltonian_type == "Tritanomaly":
            # Partial S cone dysfunction
            S = (1 - severity) * S + severity * ((M + L) / 2)

        elif self.__daltonian_type == "Achromatopsia":
            # Complete color blindness (rod vision only)
            rod_response = np.exp(-((wavelength - 498)**2) / (2 * 35**2))
            S = M = L = rod_response

        # Normalize sensitivities
        total = S + M + L
        if total > 0:
            S, M, L = S/total, M/total, L/total
        
        return S, M, L

    def simulate(self) -> np.ndarray:
        """
        Simulate color vision deficiency by applying modified cone sensitivities.
        
        Returns:
            np.ndarray: RGB image simulating the specified color vision deficiency,
                       normalized to [0,1] range
        """
        height, width = self._image_ms.get_size()[::-1]
        rgb_image = np.zeros((height, width, 3))
        
        # Process each spectral band
        for band in self._image_ms.get_bands():
            band_data = band.get_shade_of_grey().astype(float) / 255.0
            wavelength = band.get_wavelength()[0]
            S, M, L = self.calculate_sensitivity(wavelength)
            
            # Map cone responses to RGB channels
            rgb_image[:,:,2] += band_data * S  # Blue
            rgb_image[:,:,1] += band_data * M  # Green
            rgb_image[:,:,0] += band_data * L  # Red
        
        # Normalize and apply gamma correction
        gamma = 1
        for i in range(3):
            channel_max = np.max(rgb_image[:,:,i])
            if channel_max > 0:
                rgb_image[:,:,i] = np.power(rgb_image[:,:,i] / channel_max, 1/gamma)
        
        return np.clip(rgb_image, 0, 1)
