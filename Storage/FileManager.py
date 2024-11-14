from LogicLayer.ImageMS import ImageMS
from PIL import Image 
import numpy as np
from Storage.ImageManager import ImageManager
from Exceptions.MetaDataNotFoundException import MetaDataNotFoundException


class FileManager : 
    """
    Class FileManager which allow to save or load a multispectral image
    """
    SHADE_OF_GREY : chr = 'F' # An image in a shade of grey, so an 8 bits image
    IMAGE_16BIT : chr = 'I;16'
    NUMBER_TO_CONVERT_TO_8BITS : int = 256 
    MAX_COLOR_BITS : int = 255
    WAVELENGTH_LABEL : str = "Center wavelengths:"
    TABULATION_SYMBOL : chr = '\t\t'

    def __init__(self) : 
        """
        Default constructor of FileManager class
        """
        pass 
    
    @staticmethod
    def Save(image : ImageMS) -> None : 
        """
        Static method which allow to save an image 
        Parameters : 
            - the image created by the simulation, which is an instance of the ImageMS class 
        """
        pass

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
        metadata = FileManager.open_and_get_metadata(metadata_path, image_path)
        image_ms = FileManager.open_and_get_image_and_bands_data(image_path, metadata)
        return image_ms

    
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
                if ((image_name_found) and (FileManager.WAVELENGTH_LABEL in line)) :
                    wavelengths_found = True 
                    continue
                if ((wavelengths_found) and (line.strip()) and (line.startswith(FileManager.TABULATION_SYMBOL))) : 
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
        image = Image.open(image_path)
        bands = []
        print(image.n_frames)
        for num_band in range (1, image.n_frames) :
            image.seek(num_band)
            band_shade = np.array(image)
            match image.mode : 
                case FileManager.SHADE_OF_GREY : 
                    band_shade = np.array(image)*FileManager.MAX_COLOR_BITS
                case FileManager.IMAGE_16BIT : 
                    band_shade = np.array(image)/FileManager.NUMBER_TO_CONVERT_TO_8BITS
            # Use num_band - 1 to align with wavelengths array
            wavelength_index = num_band - 1
            band = ImageManager.create_band_instance([
                        num_band,  # Keep original band number
                        band_shade,
                        (metadata[wavelength_index], metadata[wavelength_index])])
            bands.append(band)
        image_ms = ImageManager.create_imagems_instance([image_path, metadata[0], metadata[-1], image.size, bands])
        return image_ms