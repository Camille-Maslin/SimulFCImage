class EmptyRGBException(Exception):
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
        self.__message = message
        super().__init__() 
    
    def __str__(self) -> str : 
        """
        Method __str__() which allow to display the exception message
        @return : str 
        Author : Lakhdar Gibril
        """
        return self.__message