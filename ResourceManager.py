class ResourceManager : 
    """
    Class which contains as constants all the necessary values for the application to avoid magic values
    Author : Lakhdar Gibril
    """
    SHADE_OF_GREY : chr = 'F' # An image in a shade of grey, so an 8 bits image
    IMAGE_16BIT : chr = 'I;16'
    NUMBER_TO_CONVERT_TO_8BITS : int = 256 
    MAX_COLOR_BITS : int = 255
    WAVELENGTH_LABEL : str = "Center wavelengths:"
    TABULATION_SYMBOL : chr = '\t\t'
    
    # Simulations Types 
    RGB_BANDS : str = "RGB bands choice"
    TRUE_COLOR : str = "True color simulation"
    BEE_COLOR : str = "Bee color simulation"
    DALTONIAN : str = "Daltonian color simulation" 

    # Paths 
    ASSETS_PATH : str = "HMI/assets/"
    DEFAULT_IMAGE : str = f"{ASSETS_PATH}no-image.1024x1024.png"
    IUT_LOGO : str = f"{ASSETS_PATH}Logo-iut-dijon-auxerre-nevers.png"
    IMVIA_LOGO : str = f"{ASSETS_PATH}Logo-laboratoire-ImViA.png"

    # Display parameters
    WINDOW_TITLE : str = "SimulFCImage"

    # Image Size
    DEFAULT_IMAGE_SIZE : tuple = (400, 400)
    LOGO_SIZE : tuple = (150, 80)
    MIN_IMAGE_SIZE = (300, 300)
    MAX_IMAGE_SIZE = (800, 800)

    # Styles
    BACKGROUND_COLOR : str = "white"
    FONT_FAMILY : str = "Arial"
    FONT_SIZES : dict = {
        "title": 14,
        "normal": 10,
        "button": 10
    }