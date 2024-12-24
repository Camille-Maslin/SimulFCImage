class ErrorMessages:
    """
    Class containing all error messages constants for the application.
    These messages are used throughout the application to provide consistent error feedback.
    """
    # File import errors
    METADATA_REQUIRED = "Metadata file is required. Import cancelled."
    IMAGE_REQUIRED = "Image file is required. Import cancelled."
    UNSUPPORTED_FORMAT = "Unsupported image format. Please use a supported file type."
    METADATA_ERROR = "Missing metadata in file. Please ensure all required labels are present."
    
    # Operation errors
    IMPORT_FIRST = "No image loaded. Please import an image first."
    INVALID_BAND_NUMBER = "Invalid band number. Please check the entered values are within range."
    BAND_NUMBER_TYPE = "Band number must be an integer value."
    
    # RGB simulation errors
    INVALID_RGB_VALUES = "Invalid RGB values. Please enter valid band numbers."
    ENTER_ALL_RGB_VALUES = "Please specify values for all RGB bands."