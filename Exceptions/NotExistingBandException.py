from Exceptions.BaseException import BaseException

class NotExistingBandException(BaseException): 
    """
    Exception which is raised when the input value of the band number is nonexistent
    Author : Lakhdar Gibril
    """

    def __init__(self, message : str) : 
        """
        Natural constructor of NotExistingBandException class
        Parameters : 
            - message : a string of the error message 
        Author : Lakhdar Gibril     
        """
        super().__init__(message) 
