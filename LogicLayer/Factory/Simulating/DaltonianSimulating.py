from LogicLayer.Factory.Simulating.SimulatingMethod import SimulateMethod
import numpy as np

class DaltonianSimulating(SimulateMethod):
    def __init__(self, image_ms, daltonian_type="Deuteranopia"):
        super().__init__(image_ms)
        self.__daltonian_type = daltonian_type

    def calculate_sensitivity(self, wavelength : float) -> tuple :
        """
        Calculation of cone sensitivity based on:
        - Brettel et al. (1997) for dichromatic vision
        - Machado et al. (2009) for anomalous trichromatic vision
        - Carroll et al. (2004) for severity ratios

        Args:
            wavelength (float): Wavelength in nanometers
            
        @returns: tuple Sensitivities (Blue, Green, Red) 
        """
        # Base sensitivities (using Stockman & Sharpe 2000 peaks)
        S = np.exp(-((wavelength - 441.8)**2) / (2 * 28**2)) * self._color_balance['B']
        M = np.exp(-((wavelength - 541.2)**2) / (2 * 38**2)) * self._color_balance['G']
        L = np.exp(-((wavelength - 566.8)**2) / (2 * 48**2)) * self._color_balance['R']

        if self.__daltonian_type == "Deuteranopia":
            # Complete absence of M cones
            # Brettel ratio: 1.0L + 0.0M + 0.0S for λ > 545nm
            #                0.0L + 0.0M + 1.0S for λ < 545nm
            M = 0.95 * L + 0.05 * S if wavelength > 545 else 0.05 * L + 0.95 * S

        elif self.__daltonian_type == "Protanopia":
            # Complete absence of L cones
            # Brettel ratio: 0.0L + 1.0M + 0.0S for λ > 545nm
            #                0.0L + 0.0M + 1.0S for λ < 545nm
            L = 0.95 * M + 0.05 * S if wavelength > 545 else 0.05 * M + 0.95 * S

        elif self.__daltonian_type == "Tritanopia":
            # Complete absence of S cones
            # Brettel ratio: 0.0S + 0.5M + 0.5L
            S = 0.5 * M + 0.5 * L

        elif self.__daltonian_type == "Deuteranomaly":
            # Machado: Partial M cone dysfunction
            severity = 0.75  # 75% severity is more common
            M = (1 - severity) * M + severity * L

        elif self.__daltonian_type == "Protanomaly":
            # Machado: Partial L cone dysfunction
            severity = 0.75
            L = (1 - severity) * L + severity * M

        elif self.__daltonian_type == "Tritanomaly":
            # Machado: Partial S cone dysfunction
            severity = 0.75
            S = (1 - severity) * S + severity * ((M + L) / 2)

        elif self.__daltonian_type == "Achromatopsia":
            # Complete color blindness
            # Peak sensitivity of rods at 498nm (Kraft et al. 1993)
            rod_response = np.exp(-((wavelength - 498)**2) / (2 * 35**2))
            return rod_response, rod_response, rod_response

        # Relative normalization
        total = S + M + L
        if total > 0:
            S, M, L = S/total, M/total, L/total
        
        return S, M, L

    def simulate(self) -> np.ndarray:
        height, width = self._image_ms.get_size()[::-1]
        rgb_image = np.zeros((height, width, 3))
        
        for band in self._image_ms.get_bands():
            band_data = band.get_shade_of_grey().astype(float) / 255.0
            wavelength = band.get_wavelength()[0]
            S, M, L = self.calculate_sensitivity(wavelength)
            
            rgb_image[:,:,2] += band_data * S  # Blue
            rgb_image[:,:,1] += band_data * M  # Green
            rgb_image[:,:,0] += band_data * L  # Red
        
        # Normalization and gamma correction
        gamma = 1
        for i in range(3):
            if np.max(rgb_image[:,:,i]) > 0:
                rgb_image[:,:,i] = rgb_image[:,:,i] / np.max(rgb_image[:,:,i])
                rgb_image[:,:,i] = np.power(rgb_image[:,:,i], 1/gamma)
        
        return np.clip(rgb_image, 0, 1)
