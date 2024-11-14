from LogicLayer.ImageMS import ImageMS
from PIL import Image 
import numpy as np
from Storage.ImageManager import ImageManager


class FileManager : 
    """
    Class FileManager which allow to save or load a multispectral image
    """
    SHADE_OF_GREY : chr = 'F' # An image in a shade of grey, so an 8 bits image
    _16BIT_IMAGE : chr = 'I;16'
    NUMBER_TO_CONVERT_TO_8BITS : int = 256 
    MAX_COLOR_BITS : int = 255

    def __init__(self) : 
        """
        Default constructor of FileManager class
        """
        pass 
    
    @staticmethod
    def Save(image : ImageMS) -> None : 
        """
        Static method which allow to save an image 
        Parameters : 
            - the image created by the simulation, which is an instance of the ImageMS class 
        """
        pass

    @staticmethod
    def Load(image_path: str, metadata_path: str) -> ImageMS:
        """
        Static method which allows loading an Image and its metadata from files selected by the user 
        Args : 
            - image_path (str) : the absolute path of the image as a string
            - metadata_path (str) : the absolute path of the metadata .txt file
        @returns : an ImageMS class object
        Author : Lakhdar Gibril
        Author : Paris Alexis (first version of the method)
        Author : Moreau Alexandre
        Author : Maslin Camille 
        """
        try:
            # Load the image
            print(f"Loading image from: {image_path}")
            image = Image.open(image_path)
            bands = []
            
            # Read wavelengths from metadata file
            print(f"Loading metadata from: {metadata_path}")
            wavelengths = []
            with open(metadata_path, 'r') as f:
                found_wavelengths = False
                found_image = False
                image_path_last = image_path.split('/')[-1]
                for line in f:
                    if image_path_last+":" in line:
                        print("Found ",image_path_last," section")
                        found_image = True
                        continue
                    if found_image and 'Center wavelengths:' in line:
                        print("Found Center wavelengths section")
                        found_wavelengths = True
                        continue
                    if found_wavelengths and line.strip() and line.startswith('\t\t'):
                        try:
                            values = [float(val) for val in line.strip().split()]
                            wavelengths.extend(values)
                            print(f"Added wavelengths: {values}")
                        except ValueError as e:
                            print(f"Error parsing wavelengths from line: {line.strip()}")
                            print(f"Error details: {str(e)}")
                    elif found_wavelengths and not line.startswith('\t\t'):
                        break
                    
            print(f"Total wavelengths found: {len(wavelengths)}")
            
            if not wavelengths:
                raise ValueError("No wavelength data found in the metadata file")
            
            # Create bands with corresponding wavelengths
            print(f"Creating bands for image with {image.n_frames} frames")
            # Skip first frame/band as it's not relevant
            for num_band in range(1, image.n_frames):
                try:
                    image.seek(num_band)  # Get the band data
                    band_shade = np.array(image)
                    match image.mode : 
                        case FileManager.SHADE_OF_GREY : 
                            band_shade = np.array(image)*FileManager.MAX_COLOR_BITS
                        case FileManager._16BIT_IMAGE : 
                            band_shade = np.array(image)/FileManager.NUMBER_TO_CONVERT_TO_8BITS
 
                    # Use num_band - 1 to align with wavelengths array
                    wavelength_index = num_band - 1
                    band = ImageManager.create_band_instance([
                        num_band,  # Keep original band number
                        band_shade,
                        (wavelengths[wavelength_index], wavelengths[wavelength_index])
                    ])
                    bands.append(band)
                    print(f"Created band {num_band} with wavelength {wavelengths[wavelength_index]}")
                except Exception as e:
                    print(f"Error creating band {num_band}: {str(e)}")
                    raise

            start_wavelength = wavelengths[0]
            end_wavelength = wavelengths[-1]
            print(f"Start wavelength: {start_wavelength}, End wavelength: {end_wavelength}")
            
            image_ms = ImageManager.create_imagems_instance([image_path, start_wavelength, end_wavelength, image.size, bands])
            print("Successfully created ImageMS instance")
            return image_ms
            
        except Exception as e:
            print(f"Error in Load method: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print("Full traceback:")
            traceback.print_exc()
            raise

        