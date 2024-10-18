import numpy as np

class Band: 
    """
    Class Band which represents the band of a multispectral image 
    
    Author : Lakhdar Gibril
    """

    def __init__(self, number : int, shade_of_grey : np.ndarray, wave_length : tuple) : 
        """
        Natural constructor of the class Band
        args: 
            - shade_of_length: an integer which represents the shade of grey, value between 0 and 255
            - wave_length: represents the wave_length of the band as a tuple of int
        
        Author : Lakhdar Gibril
        """
        self.__number = number
        self.__shade_of_grey = shade_of_grey
        self.__wave_length = wave_length

    def get_shade_of_grey (self) -> np.ndarray :
        """
        Getter which allow getting the value of the shade of grey 
        @return : the shade of grey as an integer

        Author : Lakhdar Gibril
        """ 
        return self.__shade_of_grey


    def get_wavelength (self) -> tuple : 
        """
        Getter which allows getting the wavelength of the band
        @return: tuple of int containing two wavelengths of the band

        Author : Lakhdar Gibril
        """
        return self.__wave_length
    
    def get_number(self) -> int : 
        """
        Getter which allows getting the number of the band
        @return: the number of the band as an int

        Author : Alexandre Moreau
        """
        return self.__number