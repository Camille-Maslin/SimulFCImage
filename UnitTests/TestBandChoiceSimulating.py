import unittest
import numpy as np
from unittest.mock import MagicMock
from Factory.Simulating.BandChoiceSimulating import BandChoiceSimulating
from LogicLayer.ImageMS import ImageMS

class TestBandChoiceSimulating(unittest.TestCase):
    """
    Test suite for BandChoiceSimulating class functionalities.
    Author: Alexis Paris
    """

    def setUp(self):
        """
        Setup environment for the tests by mocking the required ImageMS and Band objects.
        """
        # Mock band objects
        self.mock_band_red = MagicMock()
        self.mock_band_red.get_shade_of_grey.return_value = np.array([[10, 20], [30, 40]])

        self.mock_band_green = MagicMock()
        self.mock_band_green.get_shade_of_grey.return_value = np.array([[50, 60], [70, 80]])

        self.mock_band_blue = MagicMock()
        self.mock_band_blue.get_shade_of_grey.return_value = np.array([[90, 100], [110, 120]])

        # Create a list of mocked bands
        self.mock_bands = (self.mock_band_red, self.mock_band_green, self.mock_band_blue)

        # Mock ImageMS object
        self.mock_image_ms = MagicMock(spec=ImageMS)

        # Instantiate BandChoiceSimulating
        self.simulator = BandChoiceSimulating(self.mock_image_ms, self.mock_bands)

    def test_simulate(self):
        """
        Test the simulate method of BandChoiceSimulating.
        """
        expected_red = (np.array([[10, 20], [30, 40]]) - 10) / (40 - 10)
        expected_green = (np.array([[50, 60], [70, 80]]) - 50) / (80 - 50)
        expected_blue = (np.array([[90, 100], [110, 120]]) - 90) / (120 - 90)

        expected_rgb = np.dstack((expected_red, expected_green, expected_blue))

        result = self.simulator.simulate()

        # Verify the output matches the expected result
        np.testing.assert_array_almost_equal(result, expected_rgb, decimal=5)

    def test_band_shade_calls(self):
        """
        Test that get_shade_of_grey is called on the bands during the simulation.
        """
        self.simulator.simulate()
        self.mock_band_red.get_shade_of_grey.assert_called_once()
        self.mock_band_green.get_shade_of_grey.assert_called_once()
        self.mock_band_blue.get_shade_of_grey.assert_called_once()

if __name__ == '__main__':
    unittest.main()
