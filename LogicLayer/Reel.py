import numpy as np

class Reel : 
    """
    Class Reel which represent the reel of a multispecral image 
    
    Author : Lakhdar Gibril
    """

    def __init__(self, shade_of_grey : np.ndarray, wave_length : tuple) : 
        """
        Natural constructor of the class Reel
        args : 
            - shade_of_length : an integer which represent the shade of grey, value between 0 and 255
            - wave_length : represent the wave_length of the reel as a tuple of int
        
        Author : Lakhdar Gibril
        """
        self.__shade_of_grey = shade_of_grey
        self.__wave_length = wave_length

    def get_shade_of_grey (self) -> np.ndarray :
        """
        Getter which allow to get the value of the shade of grey 
        @return : the shade of grey as an integer

        Author : Lakhdar Gibril
        """ 
        return self.__shade_of_grey


    def get_wavelength (self) -> tuple : 
        """
        Getter which allow to get the wavelength of the reel
        @return : tuple of int containing two wavelength of the reel

        Author : Lakhdar Gibril
        """
        return self.__wave_length