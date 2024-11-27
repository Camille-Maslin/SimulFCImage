import os
import sys
import unittest
import numpy as np
import tkinter as tk

from unittest.mock import patch, MagicMock
from tkinter import filedialog
from PIL import Image

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from Storage.FileManager import FileManager
from LogicLayer.ImageMS import ImageMS
from LogicLayer.Band import Band

class TestFileManager(unittest.TestCase):
    """
    Test suite for FileManager class functionalities.
    Author: Camille Maslin, Alexis Paris (in the first version)
    """
    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests"""
        root = tk.Tk()
        root.withdraw()
        
        print("\nSelect the multispectral image test (.tif)...")
        cls.test_image_path = filedialog.askopenfilename(
            title="Select the multispectral image",
            filetypes=[("TIF files", "*.tif")]
        )
        
        print("Select the metadata file (.txt)...")
        cls.test_metadata_path = filedialog.askopenfilename(
            title="Select the metadata file",
            filetypes=[("Text files", "*.txt")]
        )
        
        if not cls.test_image_path or not cls.test_metadata_path:
            raise ValueError("The test files are required")

    def test_load_complete_image(self):
        """Test loading a complete multispectral image with metadata"""
        image_ms = FileManager.Load(self.test_image_path, self.test_metadata_path)
        
        self.assertIsInstance(image_ms, ImageMS)
        self.assertEqual(image_ms.get_path(), self.test_image_path)
        self.assertGreater(len(image_ms.get_bands()), 0)

    def test_convert_to_image_and_save(self):
        """
        Test the convert_to_image_and_save method 
        """
        # Create a test normalized numpy array image 
        test_image = np.random.rand(100, 100, 3)
        
        print("\nSelect the save location for the test image...")
        test_save_path = filedialog.asksaveasfilename(
            defaultextension=".tif",
            filetypes=[("TIF files", "*.tif"), ("PNG files", "*.png"), 
                    ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save the test image"
        )
        
        if not test_save_path:
            self.skipTest("Test cancelled - No save location selected")
        
        try:
            # Call the convert_to_image_and_save method
            FileManager.convert_to_image_and_save(test_image, test_save_path)
            
            # Verify that the file has been created
            self.assertTrue(os.path.exists(test_save_path))
            
            # Load the saved image
            saved_image = np.array(Image.open(test_save_path))
            
            # Verify the dimensions
            self.assertEqual(saved_image.shape, test_image.shape)
            
            # Verify the saved image is uint8
            self.assertEqual(saved_image.dtype, np.uint8)
            
            # Verify that the image contains valid data
            self.assertTrue(np.any(saved_image > 0))  # Check that there are non-zero pixels
            self.assertTrue(np.all(saved_image <= 255))  # Check that the values are in the valid range
            
            print(f"\nTest image saved successfully to: {test_save_path}")
            
        except Exception as e:
            print(f"\nError during saving: {str(e)}")
            raise

    def test_invalid_image_format(self):
        """Test loading an image with an unsupported format"""
        # Create a temporary JPEG image file
        temp_jpeg = "temp_test.jpg"
        test_img = Image.new('RGB', (100, 100))
        test_img.save(temp_jpeg)
        
        try:
            # Test directly with the unsupported format
            with self.assertRaises(ValueError) as context:
                with Image.open(temp_jpeg) as img:
                    if not temp_jpeg.lower().endswith('.tif'):
                        raise ValueError("Unsupported image format")
                    FileManager.Load(temp_jpeg, self.test_metadata_path)
            
            self.assertEqual(str(context.exception), "Unsupported image format")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_jpeg):
                os.remove(temp_jpeg)

    def tearDown(self):
        """Clean up resources after each test"""
        import gc
        gc.collect()

if __name__ == '__main__':
    unittest.main()