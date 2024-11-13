from LogicLayer.ImageMS import ImageMS
from PIL import Image 
import numpy as np
from Storage.ImageManager import ImageManager

class FileManager : 
    """
    Class FileManager which allow to save or load a multispectral image
    """

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
                for line in f:
                    if 'Center wavelengths:' in line:
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
                    if(image.mode == 'F'):
                        band_shade = np.array(image)*255
                    elif(image.mode == 'I;16'):
                        band_shade = np.array(image)/2**8
                    
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

        