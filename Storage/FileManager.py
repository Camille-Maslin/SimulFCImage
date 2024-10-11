import os 
import LogicLayer.ImageMS
import LogicLayer.Reel

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
    def Load() -> LogicLayer.ImageMS : 
        """
        Static method which allow to load an Image from a directory selected by the user 
        @return : an ImageMS object
        
        Author : 
        """ 
        pass 
        

