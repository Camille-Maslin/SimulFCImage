import unittest
import numpy as np
from unittest.mock import MagicMock
from Factory.Simulating.BeeSimulating import BeeSimulating
from LogicLayer.ImageMS import ImageMS

class TestBeeSimulating(unittest.TestCase):
    """
    Test suite for BeeSimulating class functionalities.
    
    Author: Paris Alexis
    """
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create ImageMS mock
        self.mock_image_ms = MagicMock(spec=ImageMS)
        self.mock_image_ms.get_size.return_value = (10, 10)  # width, height
        
        # Create simulated bands with different wavelengths matching bee vision peaks
        band1 = MagicMock()
        band1.get_wavelength.return_value = (344, 344)  # UV peak for bees
        band1.get_shade_of_grey.return_value = np.ones((10, 10)) * 0.5
        
        band2 = MagicMock()
        band2.get_wavelength.return_value = (436, 436)  # Blue peak for bees
        band2.get_shade_of_grey.return_value = np.ones((10, 10)) * 0.7
        
        band3 = MagicMock()
        band3.get_wavelength.return_value = (544, 544)  # Green peak for bees
        band3.get_shade_of_grey.return_value = np.ones((10, 10)) * 0.3
        
        self.mock_image_ms.get_bands.return_value = [band1, band2, band3]
        
        self.bee_sim = BeeSimulating(self.mock_image_ms)

    def test_initialization(self):
        """Test proper initialization of BeeSimulating."""
        self.assertIsInstance(self.bee_sim, BeeSimulating)
        color_balance = self.bee_sim._color_balance
        self.assertEqual(color_balance['R'], 1.0)
        self.assertEqual(color_balance['G'], 1.0)
        self.assertEqual(color_balance['B'], 1.0)

    def test_calculate_photoreceptor_sensitivity(self):
        """Test photoreceptor sensitivity calculations."""
        # Test UV wavelength (344nm - bee UV peak)
        UV, Blue, Green = self.bee_sim.calculate_sensitivity(344)
        self.assertGreater(UV, Blue)  # UV sensitivity should be highest
        self.assertGreater(UV, Green)
        
        # Test Blue wavelength (436nm - bee Blue peak)
        UV, Blue, Green = self.bee_sim.calculate_sensitivity(436)
        self.assertGreater(Blue, UV)  # Blue sensitivity should be highest
        self.assertGreater(Blue, Green)
        
        # Test Green wavelength (544nm - bee Green peak)
        UV, Blue, Green = self.bee_sim.calculate_sensitivity(544)
        self.assertGreater(Green, UV)  # Green sensitivity should be highest
        self.assertGreater(Green, Blue)
        
        # Test normalization - sum should equal 1
        UV, Blue, Green = self.bee_sim.calculate_sensitivity(400)
        self.assertAlmostEqual(UV + Blue + Green, 1.0, places=7)

    def test_simulate(self):
        """Test the complete simulation process."""
        # Create simulated bands with different wavelengths matching bee vision peaks
        band1 = MagicMock()
        band1.get_min_wavelength.return_value = 344
        band1.get_shade_of_grey_as_float.return_value = np.ones((10, 10)) * 0.5

        band2 = MagicMock()
        band2.get_min_wavelength.return_value = 436
        band2.get_shade_of_grey_as_float.return_value = np.ones((10, 10)) * 0.7

        band3 = MagicMock()
        band3.get_min_wavelength.return_value = 544
        band3.get_shade_of_grey_as_float.return_value = np.ones((10, 10)) * 0.3

        self.mock_image_ms.get_bands.return_value = [band1, band2, band3]
        self.mock_image_ms.get_height.return_value = 10
        self.mock_image_ms.get_width.return_value = 10

        # Run simulation
        result = self.bee_sim.simulate()
        
        # Check output shape matches expected dimensions
        self.assertEqual(result.shape, (10, 10, 3))
        
        # Verify values are properly normalized between 0 and 1
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 1))
        
        # Check output data type is float64
        self.assertEqual(result.dtype, np.float64)
        
        # Verify all bands were properly accessed during simulation
        for band in self.mock_image_ms.get_bands():
            band.get_min_wavelength.assert_called()
            band.get_shade_of_grey_as_float.assert_called()

    def test_wavelength_extremes(self):
        """Test simulation behavior with extreme wavelengths."""
        # Create bands with extreme wavelengths
        band_extreme1 = MagicMock()
        band_extreme1.get_min_wavelength.return_value = 300  # Deep UV
        band_extreme1.get_shade_of_grey_as_float.return_value = np.ones((10, 10)) * 0.5
        
        band_extreme2 = MagicMock()
        band_extreme2.get_min_wavelength.return_value = 650  # Deep Red
        band_extreme2.get_shade_of_grey_as_float.return_value = np.ones((10, 10)) * 0.5
        
        self.mock_image_ms.get_bands.return_value = [band_extreme1, band_extreme2]
        self.mock_image_ms.get_height.return_value = 10
        self.mock_image_ms.get_width.return_value = 10
        
        # Simulation should still work with extreme wavelengths
        result = self.bee_sim.simulate()
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, (10, 10, 3))

if __name__ == '__main__':
    unittest.main() 