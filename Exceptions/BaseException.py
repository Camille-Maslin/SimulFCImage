class BaseException(Exception): 
    """
    Exception which is the basic exception inherited by all exceptions
    Author : Alexandre Moreau
    """

    def __init__(self, message : str) : 
        """
        Natural constructor of SimulFCImageException class
        Parameters : 
            - message : a string of the error message 
        Author : Alexandre Moreau     
        """
        super().__init__()
        self.__message = message
    
    def __str__(self) -> str : 
        """
        Method __str__() which allow to display the exception message
        @return : str 
        Author : Alexandre Moreau
        """
        return self.__message