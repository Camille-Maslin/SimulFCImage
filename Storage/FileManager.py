from LogicLayer.ImageMS import ImageMS
from PIL import Image 
import numpy as np
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
    def Load(path : str) -> ImageMS : 
        """
        Static method which allows loading an Image from a directory selected by the user 
        args : 
            - path (str) : represent the path of the image as a string
        @return : an ImageMS object

        Author: Alexis Paris
        Author : Lakhdar Gibril
        """ 
        image = Image.open(path)
        bands = []
        for num_band in range (1,image.n_frames) :
            image.seek(num_band) # Allow to go to the specified band
            band_shade = np.array(image)/2**8 # Convert image 24 bit to 8 bit
            # We don't know how to get the wavelenght data so it is an empty tuple for now
            band = ImageManager.create_band_instance([num_band,band_shade,(1,1)]) 
            bands.append(band) 
        # We don't know how to get the wavelenght data so it is just 0 for start and end wavelenght for now
        image_ms = ImageManager.create_imagems_instance([path,0,0,image.size,bands])
        return image_ms     

        