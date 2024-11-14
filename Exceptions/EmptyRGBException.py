class EmptyRGBException(Exception):
    """
    Exception raised when RGB values are not all specified.
    
    Author : Camille Maslin
    """
    def __init__(self, message="All RGB values must be specified"):
        self.message = message
        super().__init__(self.message) 