from PIL import Image
from LogicLayer.Reel import Reel

class ImageMS (Image.Image) : 
    """
    Class ImageMS which represent a multispectral image and which inherit of the Image class

    Author : Lakhdar Gibril
    """

    def __init__(self, name : str, start_wavelength : int, end_wavelength : int, size : tuple, reels : list) : 
        """
        Natural constructor of the class ImageMS
        args : 
            - name : the image name as a string (with the path)
            - start_wavelength : an integer which represent the start wavelength of the multispectral image
            - end_wavelength : an integer which represent the end wavelength of the multispectral image
            - size : a tuple with the height and width of the image
            - reels : represent the list of reels in the image

        Author : Lakhdar Gibril
        """
        super().__init__
        self.__path = name 
        self.__start_wavelength = start_wavelength
        self.__end_wavelength = end_wavelength
        self.__reels = reels
        self.__size = size
        self.__current = self.__reels[0] # Represent the current reel

    def get_name(self) -> str : 
        """
        Getter which allow to return the name of the Image without the path 
        @return : the name of the image as a string

        Author : Lakhdar Gibril
        """
        return self.__path.split("/")[-1] 
    
    def get_start_wavelength(self) -> int : 
        """
        Getter which allow to return the wavelength start of the image
        @return : the start wavelength as an integer
        
        Author : Lakhdar Gibril
        """
        return self.__start_wavelength
    
    def get_end_wavelength(self) -> int :
        """
        Getter which allow to return the end wavelength of the image
        @return : the end wavelength as an integer

        Author : Lakhdar Gibril
        """ 
        return self.__end_wavelength

    def get_actualreel(self) -> Reel :
        """
        Getter which allow to return the actual reel of the image
        @return : the actual reel as a Reel class object

        Author : Lakhdar Gibril
        """
        return self.__current

    def set_actualreel(self, number : int) -> None : 
        """
        Setter which allow to set a new actual reel of the image
        args : 
            - reel : a Reel object to set the new current reel

        Author : Lakhdar Gibril
        """
        self.__current = self.__reels[number - 1] # So the reel index will not be out of range

    def get_reels(self) -> list : 
        """
        Getter which allow to get all the reels of the multispectral image
        @return : a list of reels object

        Author : Lakhdar Gibril
        """
        return self.__reels
    
    def get_number_reels(self) -> int : 
        """
        Getter which allow to get the number of reels of the image 
        @return : an interger of the number of reels

        Author : Lakhdar Gibril
        """
        return len(self.__reels)
    
    def get_size(self) -> tuple : 
        """
        Getter which allow to get the size of the image
        @return : the size of the image as a tuple

        Author : Lakhdar Gibril
        """
        return self.__size

    def get_path (self) -> str : 
        """
        Getter which allow to get the path of the image
        @return : the path as a string of the image 
        Author : Lakhdar Gibril
        """
        return self.__path

    def next_reel(self) -> None : 
        """
        Method which allow to switch to the next reel of the image and update the actual reel

        Author : Alexandre Moreau
        """ 
        current_index = self.__reels.index(self.__current)
        if current_index < len(self.__reels) - 1:
            self.__current = self.__reels[current_index + 1]
        else:
            self.__current = self.__reels[0]
        
    def previous_reel(self) -> None : 
        """
        Method which allow to switch to the previous reel of the image and update the actual reel

        Author : Alexandre Moreau
        """
        current_index = self.__reels.index(self.__current)
        if current_index > 0:
            self.__current = self.__reels[current_index - 1]
        else:
            self.__current = self.__reels[-1]
