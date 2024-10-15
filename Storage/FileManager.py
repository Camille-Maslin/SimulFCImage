from LogicLayer.ImageMS import ImageMS
import rasterio
import os
from Storage.ImageManager import ImageManager

class FileManager : 
    """
    Class FileManager which allow to save or load a multispectral image

    Author : Lakhdar Gibril
    """

    def __init__(self) : 
        """
        Default constructor of FileManager class
        Author : 
        """
        pass 
    
    @staticmethod
    def Save(image : ImageMS) -> None : 
        """
        Static method which allow to save an image 
        args : )
            - the image created by the simulation, which is an instance of the ImageMS class 

        Author : 
        """
        pass

    @staticmethod
    def Load(path : str, start_wavelength : int, end_wavelength : int, step : int) -> ImageMS : 
        """
        Static method which allow to load an Image from a directory selected by the user 
        args : 
            
        path : represent the path of the image as a string
        start_wavelength : int which means the begin wavelength of the image
        end_wavelength : int which specify the ending wavelength of the image
        step : int number which allow to say the step numbers between reels
        @return : an ImageMS object

        Author : Alexis Paris""" 
        current_wavelength = start_wavelength
        reels = []
        image = None

        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                with rasterio.open(f) as dataset :
                    wavelength = current_wavelength + step
                    reels.append(ImageManager.create_reel_instance(dataset.read(1),(current_wavelength,wavelength)))
                    current_wavelength = wavelength

                    imageData = [path, start_wavelength, end_wavelength, dataset.shape, reels]
                    image = ImageManager.create_imagems_instance(imageData)
        return image
                    


                    
                

            
            
        



        
        
        

