from Exceptions.BaseException import BaseException

class MetaDataNotFoundException(BaseException) : 
    """
    Exception which is raised when a data in a metadata .txt file is not found or does not exist
    Author : Lakhdar Gibril
    """

    def __init__(self, message : str) : 
        """
        Natural constructor of MetaDataNotFoundException class
        args : 
            - message (str) : a string of the error message 
        Author : Lakhdar Gibril     
        """
        super().__init__(message)
    