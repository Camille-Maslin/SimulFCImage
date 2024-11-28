from LogicLayer.Factory.Simulating.SimulatingMethod import SimulateMethod
import numpy as np

class HumanSimulating(SimulateMethod):
    def __init__(self, image_ms):
        super().__init__(image_ms)

    def calculate_sensitivity(self, wavelength : float) -> tuple :
        """
        Calculate the sensitivity of the three types of cones based on CIE 1931 color matching functions
        and Stockman & Sharpe (2000) cone fundamentals.
        
        Simple reminder of the formula :
        S(λ)=A*e^(-((λ−λ0)^2)/(2*σ)^2)

        Where:
        S(λ) is the relative sensitivity to the wavelength λ (in nanometers).
        A is a normalization constant (often adjusted to ensure S(λ) is between 0 and 1).
        λ0 is the central wavelength corresponding to the maximum sensitivity for each cone
        (λ0=565nm for red, λ0=535nm for green, and λ0=445nm for blue).
        σ is a characteristic width, determining the spread of the curve (e.g., σ≈40nm).

        Updated peak wavelengths and bandwidths according to:
        - L-cones (red): peak at 566.8nm
        - M-cones (green): peak at 541.2nm
        - S-cones (blue): peak at 441.8nm
        
        References:
        Stockman, A., & Sharpe, L. T. (2000). The spectral sensitivities of the middle- 
        and long-wavelength-sensitive cones derived from measurements in observers of 
        known genotype. Vision Research, 40(13), 1711-1737

        @returns: tuple Sensitivities (Blue, Green, Red) 
        """
        # S-cones (blue) - peak at 441.8nm
        S = np.exp(-((wavelength - 441.8)**2) / (2 * 28**2)) * self._color_balance['B']
        
        # M-cones (green) - peak at 541.2nm
        M = np.exp(-((wavelength - 541.2)**2) / (2 * 38**2)) * self._color_balance['G']
        
        # L-cones (red) - peak at 566.8nm
        L = np.exp(-((wavelength - 566.8)**2) / (2 * 48**2)) * self._color_balance['R']
        
        # Relative normalization to maintain color balance
        total = S + M + L
        if total > 0:
            S, M, L = S/total, M/total, L/total
            
        return S, M, L

    def simulate(self) -> np.ndarray:
        height, width = self._image_ms.get_size()[::-1]
        rgb_image = np.zeros((height, width, 3))
        
        # Accumulators for normalization
        max_values = np.zeros(3)
        min_values = np.ones(3) * float('inf')
        
        # First pass: accumulation and search for min/max
        for band in self._image_ms.get_bands():
            band_data = band.get_shade_of_grey().astype(float)
            wavelength = band.get_wavelength()[0]
            S, M, L = self.calculate_sensitivity(wavelength)
            
            rgb_image[:,:,0] += band_data * L
            rgb_image[:,:,1] += band_data * M
            rgb_image[:,:,2] += band_data * S
            
            for i in range(3):
                channel_data = rgb_image[:,:,i]
                max_values[i] = max(max_values[i], np.max(channel_data))
                min_values[i] = min(min_values[i], np.min(channel_data))
        
        # Normalization by channel with gamma correction
        gamma = 1  # Adjustment of gamma to improve contrast
        for i in range(3):
            if max_values[i] > min_values[i]:
                rgb_image[:,:,i] = ((rgb_image[:,:,i] - min_values[i]) / 
                                  (max_values[i] - min_values[i]))
                rgb_image[:,:,i] = np.power(rgb_image[:,:,i], 1/gamma)
        
        return np.clip(rgb_image, 0, 1)
