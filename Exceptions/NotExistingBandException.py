class NotExistingBandException(Exception): 
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
        super().__init__() # Calling the parent constructor
        self.__message = message
    
    def __str__(self) -> str : 
        """
        Method __str__() which allow to display the exception message
        @return : str 
        Author : Lakhdar Gibril
        """
        return self.__message