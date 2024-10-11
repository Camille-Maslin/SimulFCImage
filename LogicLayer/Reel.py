class Reel : 
    """
    Class Reel which represent the reel of a multispecral image 
    
    Author : Lakhdar Gibril
    """

    def __init__(self, shade_of_grey : int, wave_length : tuple) : 
        """
        Natural constructor of the class Reel
        args : 
            - shade_of_length : an integer which represent the shade of grey, value between 0 and 255
            - wave_length : represent the wave_length of the reel as a tuple of int
        
        Author : Lakhdar Gibril
        """
        self.__shade_of_grey = shade_of_grey
        self.__wave_length = wave_length

    def get_shade_of_grey (self) -> int :
        """
        Getter which allow to get the value of the shade of grey 
        @return : the shade of grey as an integer

        Author : Lakhdar Gibril
        """ 
        return self.__shade_of_grey

    def set_shade_of_grey (self, value : int) -> None : 
        """
        Setter which allow to set a new value for the shade of grey
        args : 
            - value : the value between 0 and 255 for the new shade of grey

        Author : Lakhdar Gibril
        """
        assert(value >= 0 and value <= 255 )
        self.__shade_of_grey = value


    def get_wavelength (self) -> tuple : 
        """
        Getter which allow to get the wavelength of the reel
        @return : tuple of int containing two wavelength of the reel

        Author : Lakhdar Gibril
        """
        return self.__wave_length