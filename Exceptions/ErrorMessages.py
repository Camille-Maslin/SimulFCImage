
class ErrorMessages:
    """
    Class which contains as constants all errors messages for the application
    Author : Alexandre Moreau
    """
    METADATA_REQUIRED = "Metadata file is required. Import cancelled."
    IMAGE_REQUIRED = "Image file is required. Import cancelled."
    UNSUPPORTED_FORMAT = "Unsupported image format."
    METADATA_ERROR = "One of the metadata is missing in your file, please check if there is a missing label in your file."
    IMPORT_FIRST = "Please import an image first." 
    INVALID_BAND_NUMBER = "Invalid band number. Please check the entered values."
    BAND_NUMBER_TYPE = "The band number must be an integer, not a string!"
    INVALID_RGB_VALUES = "Invalid RGB values. Please enter valid numbers."
    ENTER_ALL_RGB_VALUES = "Please specify all RGB values."