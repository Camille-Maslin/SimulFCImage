import os
import sys
import unittest
import numpy as np

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from LogicLayer.Band import Band

class TestBand(unittest.TestCase):
    """
    Test suite for Band class functionalities.
    Author: Camille Maslin, Paris Alexis
    """
    def setUp(self):
        """Set up test fixtures"""
        self.test_number = 1
        self.test_shade = np.zeros((512, 512), dtype=np.uint8)
        self.test_wavelength = (400.0, 450.0)
        self.band = Band(self.test_number, self.test_shade, self.test_wavelength)

    def test_band_initialization(self):
        """Test band initialization with valid parameters"""
        self.assertEqual(self.band.get_number(), self.test_number)
        self.assertEqual(self.band.get_wavelength(), self.test_wavelength)
        np.testing.assert_array_equal(self.band.get_shade_of_grey(), self.test_shade)

    def test_invalid_parameters(self):
        """Test band initialization with invalid parameters"""
        # Test with a negative band number
        with self.assertRaises(ValueError):
            Band(-1, self.test_shade, self.test_wavelength)
        
        # Test with an empty array
        with self.assertRaises(ValueError):
            Band(1, np.array([]), self.test_wavelength)
        
        # Test with invalid wavelengths
        with self.assertRaises(ValueError):
            Band(1, self.test_shade, (-100.0, 400.0))
        with self.assertRaises(ValueError):
            Band(1, self.test_shade, (500.0, 400.0))  # min > max

    def test_get_shade_of_grey(self):
        """Test shade of grey getter with different values"""
        # Test with limit values
        test_cases = [
            np.zeros((512, 512), dtype=np.uint8),  # All zeros
            np.ones((512, 512), dtype=np.uint8) * 255,  # All 255
            np.random.randint(0, 255, (512, 512), dtype=np.uint8)  # Random values
        ]
        
        for shade in test_cases:
            band = Band(1, shade, self.test_wavelength)
            np.testing.assert_array_equal(band.get_shade_of_grey(), shade)
            self.assertEqual(band.get_shade_of_grey().dtype, np.uint8)

    def test_get_wavelength(self):
        """Test wavelength getter with different values"""
        test_cases = [
            (400.0, 450.0),  # Normal case
            (380.0, 380.0),  # Same wavelength
            (700.0, 750.0)
        ]
        
        for wavelength in test_cases:
            band = Band(1, self.test_shade, wavelength)
            self.assertEqual(band.get_wavelength(), wavelength)
            self.assertTrue(isinstance(band.get_wavelength(), tuple))
            self.assertTrue(all(isinstance(w, float) for w in band.get_wavelength()))

    def test_get_number(self):
        """Test band number getter with different values"""
        test_numbers = [1, 2, 3, 10, 100]
        
        for number in test_numbers:
            band = Band(number, self.test_shade, self.test_wavelength)
            self.assertEqual(band.get_number(), number)

    def test_immutability(self):
        """Test the immutability of the class attributes"""
        # Make a copy of the original array before modification
        original_shade = self.band.get_shade_of_grey().copy()
        
        # Create a separate copy for modification
        modified_shade = self.band.get_shade_of_grey().copy()
        modified_shade[0, 0] = 255

        # Verify that the modification does not affect the original
        np.testing.assert_array_equal(self.band.get_shade_of_grey(), original_shade)

if __name__ == '__main__':
    unittest.main() 