import LogicLayer.Reel
import LogicLayer.ImageMS

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
    def create_reel_instance(data : list) -> LogicLayer.Reel : 
        """
        Method which allow to create a Reel class instance thanks to data found in the multispectral image
        args : 
            - data : list of mixed data for the Reel attributes. 

        Author : Lakhdar Gibril
        """
        pass 

    @staticmethod
    def create_imagems_instance(data : list) -> LogicLayer.ImageMS : 
        """
        Method which allow to create a ImageMS class instance thanks to data found in the multispectral image
        args : 
            - data : list of mixed data for the ImageMS class attributes. 

        Author : Lakhdar Gibril
        """
        pass 