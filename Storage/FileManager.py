from LogicLayer.ImageMS import ImageMS
import rasterio
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
    def Load(path : str) -> ImageMS : 
        """
        Static method which allow to load an Image from a directory selected by the user 
        args : 
            - path : represent the path of the image as a string
        @return : an ImageMS object
        
        Author : Lakhdar Gibril
        """ 
        # This will allow to open the folder and access to metadata 
        with rasterio.open(path) as dataset :         
        
            list_band = []
            # We get the tags of all the bands for the list
            for index in range (1, dataset.count + 1) : 
                band_metadata = dataset.tags(index)
                list_band.append(ImageManager.create_reel_instance([dataset.read(index), band_metadata.get('SPECTRAL_WAVELENGTH')]))

            # We get the tags of the first and last band
            first_band, last_band = dataset.tags(1), dataset.tags(dataset.count)
            start_wavelength = 0
            end_wavelength = 0

            if ('SPECTRAL_WAVELENGTH' in first_band) and ('SPECTRAL_WAVELENGTH' in last_band) : 
                start_wavelength, end_wavelength = first_band['SPECTRAL_WAVELENGTH'], last_band['SPECTRAL_WAVELENGTH'] 

            imageData = [path, start_wavelength, end_wavelength, dataset.shape,list_band]
            image = ImageManager.create_imagems_instance(imageData)
            return image
            
        



        
        
        

