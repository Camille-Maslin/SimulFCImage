import unittest
import numpy as np
from unittest.mock import MagicMock
from LogicLayer.Factory.Simulating.HumanSimulating import HumanSimulating
from LogicLayer.ImageMS import ImageMS

class TestHumanSimulating(unittest.TestCase):
    """
    Test suite for HumanSimulating class functionalities.

    Author : Paris Alexis
    """
    
    def setUp(self):
        """Initialize test environment before each test."""
        # Create a mock ImageMS
        self.mock_image_ms = MagicMock(spec=ImageMS)
        self.mock_image_ms.get_size.return_value = (10, 10)  # width, height
        
        # Create mock bands
        band1 = MagicMock()
        band1.get_wavelength.return_value = (450,)  # Blue wavelength
        band1.get_shade_of_grey.return_value = np.ones((10, 10)) * 0.5
        
        band2 = MagicMock()
        band2.get_wavelength.return_value = (550,)  # Green wavelength
        band2.get_shade_of_grey.return_value = np.ones((10, 10)) * 0.7
        
        band3 = MagicMock()
        band3.get_wavelength.return_value = (600,)  # Red wavelength
        band3.get_shade_of_grey.return_value = np.ones((10, 10)) * 0.3
        
        self.mock_image_ms.get_bands.return_value = [band1, band2, band3]
        
        self.human_sim = HumanSimulating(self.mock_image_ms)

    def test_initialization(self):
        """Test proper initialization of HumanSimulating."""
        self.assertIsInstance(self.human_sim, HumanSimulating)
        color_balance = self.human_sim._HumanSimulating__color_balance
        self.assertEqual(color_balance['R'], 1.0)
        self.assertEqual(color_balance['G'], 1.0)
        self.assertEqual(color_balance['B'], 1.0)

    def test_calculate_cone_sensitivity(self):
        """Test cone sensitivity calculation."""
        # Test for blue wavelength (441.8nm - peak for S-cones)
        S, M, L = self.human_sim._HumanSimulating__calculate_cone_sensitivity(441.8)
        self.assertGreater(S, M)  # Blue sensitivity should be highest
        self.assertGreater(S, L)
        
        # Test for green wavelength (541.2nm - peak for M-cones)
        S, M, L = self.human_sim._HumanSimulating__calculate_cone_sensitivity(541.2)
        self.assertGreater(M, S)  # Green sensitivity should be highest
        
        # Test for red wavelength (566.8nm - peak for L-cones)
        S, M, L = self.human_sim._HumanSimulating__calculate_cone_sensitivity(566.8)
        self.assertGreater(L, S)  # Red sensitivity should be highest
        
        # Test normalization
        S, M, L = self.human_sim._HumanSimulating__calculate_cone_sensitivity(500)
        self.assertAlmostEqual(S + M + L, 1.0, places=7)

    def test_simulate(self):
        """Test the simulation process."""
        # Run simulation
        result = self.human_sim.simulate()
        
        # Check output shape
        self.assertEqual(result.shape, (10, 10, 3))
        
        # Check if values are normalized between 0 and 1
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 1))
        
        # Check if output is float type
        self.assertEqual(result.dtype, np.float64)

if __name__ == '__main__':
    unittest.main()
