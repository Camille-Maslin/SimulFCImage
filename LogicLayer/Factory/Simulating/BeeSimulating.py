from LogicLayer.Factory.Simulating.SimulatingMethod import SimulateMethod
import numpy as np

class BeeSimulating(SimulateMethod):
    def __init__(self, image_ms):
        super().__init__(image_ms)
        # Coefficients based on Peitsch et al. (1992)
        self.__color_balance = {
            'UV': 1.0,    # Peak at 344nm
            'Blue': 1.0,  # Peak at 436nm
            'Green': 1.0  # Peak at 544nm
        }

    def __calculate_photoreceptor_sensitivity(self, wavelength):
        """
        Calculate the sensitivity of bee photoreceptors based on:
        - Menzel & Backhaus (1991): Colour vision in insects
        - Peitsch et al. (1992): Spectral input systems of hymenopteran insects
        
        Bees have three types of photoreceptors:
        - UV with peak at 344nm (±1nm) and bandwidth ~52nm
        - Blue with peak at 436nm (±3nm) and bandwidth ~68nm
        - Green with peak at 544nm (±3nm) and bandwidth ~86nm
        
        Args:
            wavelength (float): Wavelength in nanometers
            
        Returns:
            tuple: Sensitivities (UV, Blue, Green) normalized
        """
        # Sensitivity based on Peitsch et al. (1992)
        UV = np.exp(-((wavelength - 344)**2) / (2 * 26**2)) * self.__color_balance['UV']
        Blue = np.exp(-((wavelength - 436)**2) / (2 * 34**2)) * self.__color_balance['Blue']
        Green = np.exp(-((wavelength - 544)**2) / (2 * 43**2)) * self.__color_balance['Green']
        
        # Relative normalization
        total = UV + Blue + Green
        if total > 0:
            UV, Blue, Green = UV/total, Blue/total, Green/total
            
        return UV, Blue, Green

    def simulate(self) -> np.ndarray:
        """
        Simulate the vision of bees by applying the sensitivity curves
        of the photoreceptors.
        
        Returns:
            np.ndarray: Normalized RGB image representing the vision of bees
        """
        height, width = self._image_ms.get_size()[::-1]
        bee_image = np.zeros((height, width, 3))
        
        # Accumulators for normalization
        max_values = np.zeros(3)
        min_values = np.ones(3) * float('inf')
        
        # Processing each band
        for band in self._image_ms.get_bands():
            band_data = band.get_shade_of_grey().astype(float)
            wavelength = band.get_wavelength()[0]
            UV, Blue, Green = self.__calculate_photoreceptor_sensitivity(wavelength)
            
            # Representation in RGB:
            # UV -> Blue channel (for visualization)
            # Blue -> Green channel
            # Green -> Red channel
            bee_image[:,:,2] += band_data * UV     # UV represented in blue
            bee_image[:,:,1] += band_data * Blue   # Blue represented in green
            bee_image[:,:,0] += band_data * Green  # Green represented in red
            
            # Update min/max values
            for i in range(3):
                channel_data = bee_image[:,:,i]
                max_values[i] = max(max_values[i], np.max(channel_data))
                min_values[i] = min(min_values[i], np.min(channel_data))
        
        # Normalization and gamma correction
        gamma = 1
        for i in range(3):
            if max_values[i] > min_values[i]:
                bee_image[:,:,i] = ((bee_image[:,:,i] - min_values[i]) / 
                                  (max_values[i] - min_values[i]))
                bee_image[:,:,i] = np.power(bee_image[:,:,i], 1/gamma)
        
        return np.clip(bee_image, 0, 1)
