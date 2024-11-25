from LogicLayer.ImageMS import ImageMS
from PIL import Image 
import numpy as np
from Storage.ImageManager import ImageManager
from Exceptions.MetaDataNotFoundException import MetaDataNotFoundException
from ResourceManager import ResourceManager


class FileManager : 
    """
    Class FileManager which allow to save or load a multispectral image
    """

    def __init__(self) : 
        """
        Default constructor of FileManager class
        """
        pass 
    
    @staticmethod
    def convert_to_image_and_save(image : np.ndarray, path : str) -> None : 
        """
        Static method which allow to save an image 
        args : 
            - image (np.ndarray) : the simulated image to save as an np.ndarray
            - path (str) : the path to save the image
        Author : Lakhdar Gibril
        """
        # If the path does not contain an extension, add .tif by default
        if not path.lower().endswith(('.tif', '.png', '.jpg', '.jpeg')):
            path += '.tif'
        
        image_to_save = Image.fromarray((image * ResourceManager.MAX_COLOR_BITS).astype(np.uint8))
        image_to_save.save(path)

    @staticmethod
    def Load(image_path: str, metadata_path: str) -> ImageMS:
        """
        Static method which allows loading an Image and its metadata from files selected by the user 
        args : 
            - image_path (str) : the absolute path of the image as a string
            - metadata_path (str) : the absolute path of the metadata .txt file
        @returns : an ImageMS class object
        Author : Lakhdar Gibril
        Author : Paris Alexis (first version of the method)
        Author : Moreau Alexandre
        Author : Maslin Camille 
        """
        # Verify the format of the file
        if not image_path.lower().endswith('.tif'):
            raise ValueError("Unsupported image format")
        
        metadata = FileManager.open_and_get_metadata(metadata_path, image_path)
        image_ms = FileManager.open_and_get_image_and_bands_data(image_path, metadata)
        return image_ms

    
    @staticmethod
    def open_and_get_metadata(file_path : str, image_path : str) -> list :         
        """
        Method which allow to open and get the metadata of the image 
        args : 
            - file_path (str) : path of the metadata .txt file to open and read
            - image_path (str) : absolute path of the image 
        @return : a list of float number 
        Author : Lakhdar Gibril
        """
        wavelengths = []
        image_name_found = False 
        wavelengths_found = False
        with open(file_path, 'r') as meta :
            image_name = image_path.split('/')[-1] # To only get the name of the image
            for line in meta : # Reading all the line in the meta file
                if (f"{image_name}:" in line) : 
                    image_name_found = True
                    continue
                if ((image_name_found) and (ResourceManager.WAVELENGTH_LABEL in line)) :
                    wavelengths_found = True 
                    continue
                if ((wavelengths_found) and (line.strip()) and (line.startswith(ResourceManager.TABULATION_SYMBOL))) : 
                    values = [float(val) for val in line.strip().split()]
                    wavelengths.extend(values)
            if (len(wavelengths) == 0): # If none of the data were found we raise an exception
                file_name = file_path.split('/')[-1]
                raise MetaDataNotFoundException(f"One of the metadata is missing in your {file_name}, please check if there is a missing label in your file")
        return wavelengths

    def open_and_get_image_and_bands_data(image_path : str, metadata : list) -> ImageMS :
        """
        Method which allow to open and get an imported image data and her bands data too
        args : 
            - image_path (str) : path of the image to open and get the data
            - metadata (list) : list of metadata for the bands wavelength
        @return : an ImageMS object 
        Author : Lakhdar Gibril
        """
        with Image.open(image_path) as image:
            bands = []
            print(image.n_frames)
            for num_band in range(1, image.n_frames):
                image.seek(num_band)
                band_shade = np.array(image)
                match image.mode : 
                    case ResourceManager.SHADE_OF_GREY : 
                        band_shade = np.array(image)*ResourceManager.MAX_COLOR_BITS
                    case ResourceManager.IMAGE_16BIT : 
                        band_shade = np.array(image)/ResourceManager.NUMBER_TO_CONVERT_TO_8BITS
                # Use num_band - 1 to align with wavelengths array
                wavelength_index = num_band - 1
                band = ImageManager.create_band_instance([
                            num_band,  # Keep original band number
                            band_shade,
                            (metadata[wavelength_index], metadata[wavelength_index])])
                bands.append(band)
            image_ms = ImageManager.create_imagems_instance([image_path, metadata[0], metadata[-1], image.size, bands])
            return image_ms