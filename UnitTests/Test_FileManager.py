import unittest
import numpy as np
import rasterio
import os

from unittest.mock import patch, MagicMock
from Storage.FileManager import FileManager
from LogicLayer.ImageMS import ImageMS
from LogicLayer.Band import Band

"""
Class which verifies the functionality of the FileManager's methods.

Author: Alexis Paris
"""
class TestFileManager(unittest.TestCase):
    def setUp(self):
        # Basic setup for all tests - using typical wavelength values
        self.test_path = "/test/path"
        self.start_wavelength = 400
        self.end_wavelength = 700
        self.step = 100
        self.mock_image_data = np.zeros((100, 100), dtype=np.uint8)


    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('rasterio.open')
    def test_load(self, mock_rasterio_open, mock_isfile, mock_listdir):
        """
        Tests basic TIFF image loading
        """
        # Setup two test TIFF files
        mock_listdir.return_value = ['image1.tiff', 'image2.tiff']
        mock_isfile.return_value = True
        
        mock_dataset = MagicMock()
        mock_dataset.shape = (100, 100)
        mock_dataset.read.return_value = self.mock_image_data
        mock_dataset.read.return_value.dtype = "uint8"
        
        mock_rasterio_open.return_value.__enter__.return_value = mock_dataset
        
        result = FileManager.Load(
            self.test_path,
            self.start_wavelength,
            self.end_wavelength,
            self.step
        )
        
        # Asserts to check if everything loads correctly
        self.assertIsInstance(result, ImageMS)
        self.assertEqual(result.get_path(), self.test_path)
        self.assertEqual(result.get_start_wavelength(), self.start_wavelength)
        self.assertEqual(result.get_end_wavelength(), self.end_wavelength)
        self.assertEqual(len(result.get_bands()), 2)
        
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_load_with_different_extensions(self, mock_isfile, mock_listdir):
        """
        Tests loading different image formats
        """
        # Test various image formats + invalid file
        mock_listdir.return_value = ['image1.png', 'image2.jpg', 'image3.jpeg', 'invalid.txt']
        mock_isfile.return_value = True
        
        with patch('rasterio.open') as mock_rasterio_open:
            mock_dataset = MagicMock()
            mock_dataset.shape = (100, 100)
            mock_dataset.read.return_value = self.mock_image_data
            mock_dataset.read.return_value.dtype = "uint8"
            mock_rasterio_open.return_value.__enter__.return_value = mock_dataset
            
            result = FileManager.Load(
                self.test_path,
                self.start_wavelength,
                self.end_wavelength,
                self.step
            )
            
            # Asserts 
            self.assertIsInstance(result, ImageMS)
            self.assertEqual(len(result.get_bands()), 3) 

if __name__ == "__main__":
    unittest.main()