from PIL import Image

from LogicLayer.Band import Band
from Exceptions.NotExistingBandException import NotExistingBandException
from Exceptions.ErrorMessages import ErrorMessages

class ImageMS (Image.Image) : 
    """
    Class ImageMS which represent a multispectral image and which inherit of the Image class

    Author : Lakhdar Gibril
    """

    def __init__(self, name : str, start_wavelength : int, end_wavelength : int, size : tuple, bands : list) : 
        """
        Natural constructor of the class ImageMS
        args: 
            - name: the image name as a string (with the path)
            - start_wavelength: an integer which represents the start wavelength of the multispectral image
            - end_wavelength: an integer which represents the end wavelength of the multispectral image
            - size: a tuple with the height and width of the image
            - bands: represent the list of bands in the image

        Author : Lakhdar Gibril
        """
        super().__init__
        self.__path = name 
        self.__start_wavelength = start_wavelength
        self.__end_wavelength = end_wavelength
        self.__bands = bands
        self.__size = size
        self.__current = self.__bands[0]  # Represent the current band

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

    def get_actualband(self) -> Band:
        """
        Getter which allow to return the actual band of the image
        @return : the actual band as a Band class object

        Author : Lakhdar Gibril
        """
        return self.__current

    def set_actualband(self, band_number: int) -> None: 
        """
        Setter which allows to set a new actual band of the image
        args: 
            - band_number: an integer representing the band number to set as the current band
        """
        if ((1 > band_number) or (band_number > len(self.__bands))):
            raise NotExistingBandException(ErrorMessages.INVALID_BAND_NUMBER)
        else :
            self.__current = self.__bands[band_number - 1]

    def get_bands(self) -> list : 
        """
        Getter which allow to get all the bands of the multispectral image
        @return : a list of bands object

        Author : Lakhdar Gibril
        """
        return self.__bands
    
    def get_number_bands(self) -> int: 
        """
        Getter which allow to get the number of bands of the image 
        @return : an interger of the number of bands

        Author : Lakhdar Gibril
        """
        return len(self.__bands)
    
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


    def next_band(self) -> None: 
        """
        Method which allow to switch to the next band of the image and update the actual band

        Author : Alexandre Moreau
        """ 
        current_index = self.__bands.index(self.__current)
        if current_index < len(self.__bands) - 1:
            self.__current = self.__bands[current_index + 1]
        else:
            self.__current = self.__bands[0]
        

    def previous_band(self) -> None: 
        """
        Method which allow to switch to the previous band of the image and update the actual band

        Author : Alexandre Moreau
        """
        current_index = self.__bands.index(self.__current)
        if current_index > 0:
            self.__current = self.__bands[current_index - 1]
        else:
            self.__current = self.__bands[-1]
