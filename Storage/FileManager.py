import numpy as np
from PIL import Image 
import pandas as pd
from scipy.interpolate import interp1d

from Storage.ImageManager import ImageManager
from LogicLayer.ImageMS import ImageMS
from Exceptions.MetaDataNotFoundException import MetaDataNotFoundException
from Exceptions.ErrorMessages import ErrorMessages
from ResourceManager import ResourceManager


class FileManager:
    """
    Handles file operations for multispectral images, including loading, saving,
    and metadata processing.
    
    This class provides static methods for:
    - Loading multispectral images and their metadata
    - Saving processed images
    - Processing metadata files
    - Loading spectral sensitivity data
    """

    @staticmethod
    def convert_to_image_and_save(image: np.ndarray, path: str) -> None:
        """
        Convert and save a numpy array as an image file.
        
        Args:
            image (np.ndarray): Simulated image data to save
            path (str): Destination path for the saved image
        """
        image_to_save = Image.fromarray((image * ResourceManager.MAX_COLOR_BITS).astype(np.uint8))
        image_to_save.save(path)

    @staticmethod
    def Load(image_path: str, metadata_path: str) -> ImageMS:
        """
        Load a multispectral image and its metadata from files.
        
        Args:
            image_path (str): Path to the image file
            metadata_path (str): Path to the metadata file
            
        Returns:
            ImageMS: Loaded multispectral image object
            
        Raises:
            ValueError: If image format is not supported
            MetaDataNotFoundException: If metadata is missing or invalid
        """
        if not image_path.lower().endswith('.tif'):
            raise ValueError(ErrorMessages.UNSUPPORTED_FORMAT)
        
        metadata = FileManager.open_and_get_metadata(metadata_path, image_path)
        image_ms = FileManager.open_and_get_image_and_bands_data(image_path, metadata)
        return image_ms

    @staticmethod
    def open_and_get_metadata(file_path: str, image_path: str) -> list:
        """
        Extract wavelength metadata from the metadata file.
        
        Args:
            file_path (str): Path to the metadata file
            image_path (str): Path to the image file (used to match metadata)
            
        Returns:
            list: List of wavelength values
            
        Raises:
            MetaDataNotFoundException: If required metadata is not found
        """
        wavelengths = []
        image_name_found = False
        wavelengths_found = False
        
        with open(file_path, 'r') as meta:
            image_name = image_path.split('/')[-1]
            for line in meta:
                if f"{image_name}:" in line:
                    image_name_found = True
                    continue
                if image_name_found and ResourceManager.WAVELENGTH_LABEL in line:
                    wavelengths_found = True
                    continue
                if wavelengths_found and line.strip() and line.startswith(ResourceManager.TABULATION_SYMBOL):
                    values = [float(val) for val in line.strip().split()]
                    wavelengths.extend(values)
                    
        if not wavelengths:
            raise MetaDataNotFoundException(ErrorMessages.METADATA_ERROR)
        return wavelengths

    @staticmethod
    def open_and_get_image_and_bands_data(image_path: str, metadata: list) -> ImageMS:
        """
        Load image data and create band objects from a multispectral image file.
        
        Args:
            image_path (str): Path to the image file
            metadata (list): List of wavelength values for each band
            
        Returns:
            ImageMS: Multispectral image object with all bands loaded
        """
        with Image.open(image_path) as image:
            bands = []
            for num_band in range(1, image.n_frames):
                image.seek(num_band)
                band_shade = np.array(image)
                
                # Convert band data based on image mode
                if image.mode == ResourceManager.SHADE_OF_GREY:
                    band_shade = np.array(image) * ResourceManager.MAX_COLOR_BITS
                elif image.mode == ResourceManager.IMAGE_16BIT:
                    band_shade = np.array(image) / ResourceManager.NUMBER_TO_CONVERT_TO_8BITS
                
                wavelength_index = num_band - 1
                band = ImageManager.create_band_instance([
                    num_band,
                    band_shade,
                    (metadata[wavelength_index], metadata[wavelength_index])
                ])
                bands.append(band)
                
            image_ms = ImageManager.create_imagems_instance([
                image_path,
                metadata[0],
                metadata[wavelength_index],
                image.size,
                bands
            ])
            return image_ms

    @staticmethod
    def open_and_load_sensitivity_data() -> callable:
        """
        Load and create interpolation functions for cone sensitivity data.
        
        Returns:
            callable: Function that takes wavelength and returns (L, M, S) sensitivities
        """
        # Load sensitivity data from CSV
        data_path = "LogicLayer/Factory/Simulating/data/linss2_10e_fine.csv"
        data = pd.read_csv(data_path, header=None, names=['wavelength', 'L', 'M', 'S'])
        
        # Create interpolation functions
        wavelengths = data['wavelength'].values
        L_interp = interp1d(wavelengths, data['L'].values, bounds_error=False, fill_value=0)
        M_interp = interp1d(wavelengths, data['M'].values, bounds_error=False, fill_value=0)
        S_interp = interp1d(wavelengths, data['S'].values, bounds_error=False, fill_value=0)
        
        def get_sensitivities(wavelength: float) -> tuple:
            """Return interpolated cone sensitivities for a given wavelength"""
            return (float(L_interp(wavelength)),
                   float(M_interp(wavelength)),
                   float(S_interp(wavelength)))
        
        return get_sensitivities