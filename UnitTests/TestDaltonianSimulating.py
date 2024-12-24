import unittest
import numpy as np
from unittest.mock import MagicMock
from Factory.Simulating.DaltonianSimulating import DaltonianSimulating
from LogicLayer.ImageMS import ImageMS
from LogicLayer.Band import Band

class TestDaltonianSimulating(unittest.TestCase):
    """
    Test suite for DaltonianSimulating class functionalities.
    
    Author: Paris Alexis
    """
    
    def setUp(self):
        # Create a test image
        self.test_array = np.array([[100, 150], [200, 250]])
        band1 = Band(1, self.test_array.copy(), (400, 450))
        band2 = Band(2, self.test_array.copy(), (500, 550))
        band3 = Band(3, self.test_array.copy(), (600, 650))
        self.image_ms = ImageMS("test_image", 400, 650, (2, 2), [band1, band2, band3])

    def test_deuteranopia(self):
        """Test the simulation of deuteranopia"""
        # Create a simulator instance for deuteranopia color blindness
        simulator = DaltonianSimulating(self.image_ms, "Deuteranopia")
        # Generate the simulated image
        result = simulator.simulate()
        
        # Verify that the output image has the correct dimensions (height, width, RGB channels)
        self.assertEqual(result.shape, (2, 2, 3))
        # Check if all pixel values are normalized between 0 and 1
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        # Test sensitivity
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)

    def test_protanopia(self):
        """Test the simulation of protanopia"""
        simulator = DaltonianSimulating(self.image_ms, "Protanopia")
        result = simulator.simulate()
        
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)

    def test_tritanopia(self):
        """Test the simulation of tritanopia"""
        simulator = DaltonianSimulating(self.image_ms, "Tritanopia")
        result = simulator.simulate()
        
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)

    def test_deuteranomaly(self):
        """Test the simulation of deuteranomaly"""
        simulator = DaltonianSimulating(self.image_ms, "Deuteranomaly")
        result = simulator.simulate()
        
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)

    def test_protanomaly(self):
        """Test the simulation of protanomaly"""
        simulator = DaltonianSimulating(self.image_ms, "Protanomaly")
        result = simulator.simulate()
        
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)

    def test_tritanomaly(self):
        """Test the simulation of tritanomaly"""
        simulator = DaltonianSimulating(self.image_ms, "Tritanomaly")
        result = simulator.simulate()
        
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)

    def test_achromatopsia(self):
        """Test the simulation of achromatopsia"""
        simulator = DaltonianSimulating(self.image_ms, "Achromatopsia")
        result = simulator.simulate()
        
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))
        
        S, M, L = simulator.calculate_sensitivity(550)
        self.assertAlmostEqual(S + M + L, 1.0, places=5)
        self.assertAlmostEqual(S, M, places=5)
        self.assertAlmostEqual(M, L, places=5)

if __name__ == '__main__':
    unittest.main()

