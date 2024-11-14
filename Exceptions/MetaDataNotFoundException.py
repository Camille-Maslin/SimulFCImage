class MetaDataNotFoundException(Exception) : 
    """
    Exception which is raised when a data in a metadata .txt file is not found or does not exist
    Author : Lakhdar Gibril
    """

    def __init__(self, message : str) : 
        """
        Natural constructor of MetaDataNotFoundException class
        Args : 
            - message (str) : a string of the error message 
        Author : Lakhdar Gibril     
        """
        super().__init__() # Calling the parent constructor
        self.__message = message
    
    def __str__(self) -> str : 
        """
        Method __str__() which allow to display the exception message
        @return : str 
        Author : Lakhdar Gibril
        """
        return self.__message