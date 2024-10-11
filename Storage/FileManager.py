import LogicLayer.ImageMS
import LogicLayer.Reel
import rasterio
import ImageManager

class FileManager : 
    """
    Class FileManager which allow to save or load a multispectral image

    Author : 
    """

    def __init__(self) : 
        """
        Default constructor of FileManager class
        Author : 
        """
        pass 
    
    @staticmethod
    def Save(image : LogicLayer.ImageMS) -> None : 
        """
        Static method which allow to save an image 
        args : 
            - the image created by the simulation, which is an instance of the ImageMS class 

        Author : 
        """
        pass

    @staticmethod
    def Load(path : str) -> LogicLayer.ImageMS : 
        """
        Static method which allow to load an Image from a directory selected by the user 
        args : 
            - path : represent the path of the image as a string
        @return : an ImageMS object
        
        Author : Lakhdar Gibril
        """ 
        # This will allow to open the folder and access to metadata 
        with rasterio.open(path) as dataset :         
        
            # We get the tags of the first and last band
            first_band, last_band = dataset.tags(1), dataset.tags(dataset.count)

            if ("Wavelength" in first_band) and ("Wavelength" in last_band) : 
                start_wavelength, end_wavelength = first_band['Wavelength'], last_band['Wavelength'] 

            ImageManager.ImageManager.create_imagems_instance([path,start_wavelength,end_wavelength,(dataset.width,dataset.height),[]])
            
        



        
        
        

