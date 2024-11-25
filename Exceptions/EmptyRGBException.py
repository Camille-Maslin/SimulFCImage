from Exceptions.BaseException import BaseException

class EmptyRGBException(BaseException):
    """
    Exception raised when RGB values are not all specified.
    
    Author : Camille Maslin
    """
    def __init__(self, message : str = "All RGB values must be specified") :
        """
        Natural constructor of MetaDataNotFoundException class
        args : 
            - message (str) : a string of the error message 
        Author : Camille Maslin
        """
        super().__init__(message) 
    