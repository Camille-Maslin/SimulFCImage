from LogicLayer.Reel import Reel
from LogicLayer.ImageMS import ImageMS

class ImageManager : 
    """
    Class ImageManager which allow to create instance of Image when they are loaded 
    thanks to the FileManager class methods

    Author : Lakhdar Gibril
    """

    def __init__(self) : 
        """
        Natural constructor of the ImageManager class
        
        Author : Lakhdar Gibril
        """
        pass 

    @staticmethod
    def create_reel_instance(data : list) -> Reel : 
        """
        Method which allow to create a Reel class instance thanks to data found in the multispectral image
        args : 
            - data : list of mixed data for the Reel attributes. 

        Author : Lakhdar Gibril
        """
        reel = Reel(data[0],data[1])
        return reel  

    @staticmethod
    def create_imagems_instance(data : list) -> ImageMS : 
        """
        Method which allow to create a ImageMS class instance thanks to data found in the multispectral image
        args : 
            - data : list of mixed data for the ImageMS class attributes. 

        Author : Lakhdar Gibril
        """
        image = ImageMS(data[0],data[1],data[2],data[3],data[4])
        return image 