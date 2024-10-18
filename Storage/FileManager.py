from LogicLayer.ImageMS import ImageMS
import rasterio
import os
from Storage.ImageManager import ImageManager

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
    def Save(image : ImageMS) -> None : 
        """
        Static method which allow to save an image 
        Parameters : 
            - the image created by the simulation, which is an instance of the ImageMS class 
        """
        pass

    @staticmethod
    def Load(path : str, start_wavelength : int, end_wavelength : int, step : int) -> ImageMS : 
        """
        Static method which allows loading an Image from a directory selected by the user 
        Parameters : 
            path: represent the path of the image as a string
            start_wavelength: int which means the begin wavelength of the image
            end_wavelength: int which specify the ending wavelength of the image
            step: int number which allows to say the step numbers between bands
        @return: an ImageMS object

        Author: Alexis Paris
        """ 
        current_wavelength = start_wavelength
        bands = []
        image = None
        band_number = 1

        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isfile(f) and f.lower().endswith('.tiff'):
                with rasterio.open(f) as dataset:
                    wavelength = current_wavelength + step
                    bands.append(ImageManager.create_band_instance([band_number, dataset.read(1), (current_wavelength, wavelength)]))
                    current_wavelength = wavelength
                    band_number += 1

        height, width = dataset.shape

        imageData = [path, start_wavelength, end_wavelength, (height, width), bands]
        image = ImageManager.create_imagems_instance(imageData)
        return image