from LogicLayer.Band import Band
from LogicLayer.ImageMS import ImageMS

class ImageManager : 
    """
    Class ImageManager which allows creating instances of Image when they are loaded 
    thanks to the FileManager class methods

    Author : Lakhdar Gibril
    """

    def __init__(self) : 
        """
        Natural constructor of the ImageManager class
        """
        pass 

    @staticmethod
    def create_band_instance(data: list) -> Band: 
        """
        Method which allows creating a Band class instance thanks to data found in the multispectral image
        Parameters : 
            - data: list of mixed data for the Band attributes.
        Author : Lakhdar Gibril
        """
        band = Band(data[0], data[1], data[2])
        return band  

    @staticmethod
    def create_imagems_instance(data : list) -> ImageMS : 
        """
        Method which allows creating an ImageMS class instance thanks to data found in the multispectral image
        Parameters : 
            - data : list of mixed data for the ImageMS class attributes.
        Author : Lakhdar Gibril
        """
        image = ImageMS(data[0],data[1],data[2],data[3],data[4])
        return image 