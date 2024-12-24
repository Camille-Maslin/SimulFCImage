from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import numpy as np
import os

from Storage.FileManager import FileManager
from LogicLayer.Factory.SimulatorFactory import SimulatorFactory
from Exceptions.ErrorMessages import ErrorMessages
from ResourceManager import ResourceManager

class MainController:
    """
    Main controller handling the interaction between UI and business logic
    """
    def __init__(self):
        self._image_ms = None
        self._simulated_image = None
        self._current_simulation = None
        
        # Initialize simulator factory
        self._factory = SimulatorFactory.instance()
        
        # Register all simulators
        from LogicLayer.Factory.CreateSimulating.CreateBandChoiceSimulating import CreateBandChoiceSimulator
        from LogicLayer.Factory.CreateSimulating.CreateHumanSimulating import CreateHumanSimulator
        from LogicLayer.Factory.CreateSimulating.CreateBeeSimulating import CreateBeeSimulator
        from LogicLayer.Factory.CreateSimulating.CreateDaltonianSimulating import CreateDaltonianSimulator
        from LogicLayer.Factory.CreateSimulating.CreateHumanConeSimulating import CreateHumanConeSimulator
        
        self._factory.register(ResourceManager.RGB_BANDS, CreateBandChoiceSimulator())
        self._factory.register(ResourceManager.TRUE_COLOR, CreateHumanSimulator())
        self._factory.register(ResourceManager.BEE_COLOR, CreateBeeSimulator())
        self._factory.register(ResourceManager.DALTONIAN, CreateDaltonianSimulator())
        self._factory.register(ResourceManager.HUMAN_CONE, CreateHumanConeSimulator())
        
        self._current_band_index = 0
        self._last_rgb_bands = None
        self._last_directory = ResourceManager.DEFAULT_IMAGE_DIRECTORY
        self._simulation_history = []  # Liste pour stocker l'historique
        
    def load_image(self):
        """
        Opens file dialogs to select image and metadata files, then loads the image
        Returns:
            bool: True if loading successful
        """
        try:
            image_path = QFileDialog.getOpenFileName(
                None,
                "Select Image File",
                self._last_directory,
                "Image Files (*.tif *.tiff)"
            )[0]
            
            if image_path:
                # Met à jour le dernier répertoire utilisé
                self._last_directory = os.path.dirname(image_path)
                
                metadata_path = QFileDialog.getOpenFileName(
                    None,
                    "Select Metadata File",
                    self._last_directory,
                    "Text Files (*.txt)"
                )[0]
                
                if metadata_path:
                    self._image_ms = FileManager.Load(image_path, metadata_path)
                    return True
                else:
                    raise ValueError(ErrorMessages.METADATA_REQUIRED)
            else:
                raise ValueError(ErrorMessages.IMAGE_REQUIRED)
                    
        except Exception as e:
            raise e
    
    def get_image_data(self):
        """
        Returns current image metadata
        """
        if not self._image_ms:
            return None
            
        return {
            'name': self._image_ms.get_name(),
            'size': f"{self._image_ms.get_size()[0]}x{self._image_ms.get_size()[1]}",
            'bands': str(self._image_ms.get_number_bands()),
            'wavelength': f"{self._image_ms.get_start_wavelength():.2f}-{self._image_ms.get_end_wavelength():.2f} nm"
        }
    
    def simulate(self, simulation_type, params=None):
        """
        Executes the selected simulation
        """
        if not self._image_ms:
            return False, ErrorMessages.IMPORT_FIRST
        
        try:
            if simulation_type == ResourceManager.DALTONIAN:
                print(f"Starting daltonism simulation with type: {params}")
                
                # For color blindness, we first need to simulate human vision
                human_simulator = self._factory.create(ResourceManager.TRUE_COLOR, self._image_ms, ())
                true_color_image = human_simulator.simulate()
                
                # On crée le simulateur de daltonisme
                simulator = self._factory.create(simulation_type, self._image_ms, (), daltonian_type=params)
                self._simulated_image = simulator.simulate()
                
                if self._simulated_image is None:
                    return False, "Simulation failed to produce an image"
                
                print(f"Final simulated image shape: {self._simulated_image.shape}")  # Debug
                
                # Vérification que le filtre a bien été appliqué
                if np.array_equal(self._simulated_image, true_color_image):
                    return False, "Daltonism filter was not properly applied"
                    
                self._current_simulation = simulation_type
                
                # Add to history
                from datetime import datetime
                history_entry = {
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'image_name': self._image_ms.get_name(),
                    'simulation_type': simulation_type,
                    'parameters': params,
                    'image': self._get_qimage_from_array(self._simulated_image)
                }
                self._simulation_history.append(history_entry)
                
                return True, None
                
            else:
                simulator = self._factory.create(simulation_type, self._image_ms, params)
                self._simulated_image = simulator.simulate()
            
            self._current_simulation = simulation_type
            
            # Store RGB bands if it's an RGB simulation
            if simulation_type == ResourceManager.RGB_BANDS:
                self._last_rgb_bands = params
            
            # Add to history
            from datetime import datetime
            history_entry = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'image_name': self._image_ms.get_name(),
                'simulation_type': simulation_type,
                'parameters': params,
                'image': self._get_qimage_from_array(self._simulated_image)  # Convertir l'image pour l'historique
            }
            self._simulation_history.append(history_entry)
            
            return True, None
        except Exception as e:
            return False, str(e)
    
    def _convert_to_uint8(self, image_array):
        """
        Safely convert float array to uint8, handling NaN values and normalization
        """
        # Replace NaN values with 0
        image_array = np.nan_to_num(image_array, nan=0.0)
        
        # Ensure values are in [0, 1] range
        image_array = np.clip(image_array, 0, 1)
        
        # Convert to uint8 [0, 255]
        return (image_array * 255.0).round().astype(np.uint8)

    def save_simulation(self):
        """
        Saves the current simulation result
        """
        # Check if simulated image exists using numpy's size check
        if self._simulated_image is None or self._simulated_image.size == 0:
            return False, "No simulation to save"
        
        # Create default filename based on original image name and simulation type
        original_name = self._image_ms.get_name().split('.')[0]  # Remove extension
        
        # Add RGB values to filename if it's an RGB simulation
        if self._current_simulation == ResourceManager.RGB_BANDS:
            # Get the last used RGB values
            rgb_values = [str(band.get_number()) for band in self._last_rgb_bands]
            default_filename = f"{original_name}_RGB_{rgb_values[0]}_{rgb_values[1]}_{rgb_values[2]}.png"
        elif self._current_simulation == ResourceManager.DALTONIAN:
            # Ajoute le type de daltonisme au nom du fichier
            daltonian_type = next((entry['parameters'] for entry in reversed(self._simulation_history) 
                                if entry['simulation_type'] == ResourceManager.DALTONIAN), None)
            default_filename = f"{original_name}_{self._current_simulation.replace(' ', '_').lower()}_{daltonian_type}.png"
        else:
            default_filename = f"{original_name}_{self._current_simulation.replace(' ', '_').lower()}.png"
        
        save_path = QFileDialog.getSaveFileName(
            None,
            "Save Simulation",
            default_filename,
            "PNG Files (*.png);;JPEG Files (*.jpg);;TIFF Files (*.tif)"
        )[0]
        
        if save_path:
            try:
                # Convert to uint8
                save_data = self._convert_to_uint8(self._simulated_image)
                
                # Convert numpy array to PIL Image
                from PIL import Image
                if len(save_data.shape) == 3:  # RGB image
                    image = Image.fromarray(save_data, 'RGB')
                else:  # Grayscale image
                    image = Image.fromarray(save_data, 'L')
                
                # Save the image
                image.save(save_path)
                return True, None
                
            except Exception as e:
                return False, str(e)
                
        return False, "Save cancelled"
    
    def has_image(self):
        """Check if an image is loaded"""
        return self._image_ms is not None
        
    def get_current_band(self):
        """Get current band number"""
        if self._image_ms:
            return self._image_ms.get_actualband().get_number()
        return 0
        
    def get_band_by_number(self, number):
        """Get band by its number"""
        if self._image_ms:
            return self._image_ms.get_band_by_number(number)
        return None
        
    def set_current_band(self, number):
        """Set the current band directly by number"""
        if self._image_ms:
            # Vérifier que le numéro est valide
            if 1 <= number <= self._image_ms.get_number_bands():
                band = self.get_band_by_number(number)
                if band:
                    self._image_ms.set_actualband(number)  # On passe le numéro au lieu de la bande
                    return True
        return False
        
    def get_total_bands(self):
        """Get total number of bands"""
        if self._image_ms:
            return self._image_ms.get_number_bands()
        return 0
        
    def next_band(self):
        """Switch to next band"""
        if self._image_ms:
            self._image_ms.next_band()
            
    def previous_band(self):
        """Switch to previous band"""
        if self._image_ms:
            self._image_ms.previous_band()
            
    def get_current_band_pixmap(self):
        """Get the current band as a QPixmap"""
        if self._image_ms:
            # Get band data and normalize it to 0-255 range
            band_data = self._image_ms.get_actualband().get_shade_of_grey()
            
            # Make sure the data is in the correct format
            if band_data.dtype != np.uint8:
                # Normalize to 0-255 range
                band_data = ((band_data - np.min(band_data)) / 
                            (np.max(band_data) - np.min(band_data)) * 255).astype(np.uint8)
            
            height, width = band_data.shape
            
            # Ensure the data is contiguous in memory
            band_data = np.ascontiguousarray(band_data)
            
            # Create QImage with the correct format and stride
            bytes_per_line = width  # For grayscale images, bytes per line equals width
            image = QImage(band_data.data, width, height, bytes_per_line, 
                          QImage.Format.Format_Grayscale8)
            
            # Convert to QPixmap and scale to fit
            pixmap = QPixmap.fromImage(image)
            return pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, 
                               Qt.TransformationMode.SmoothTransformation)
            
        return None 
    
    def get_simulated_image_pixmap(self):
        """Get the simulated image as a QPixmap"""
        if self._simulated_image is not None:
            # Convert numpy array to QImage
            height, width, channels = self._simulated_image.shape
            bytes_per_line = channels * width
            
            # Convert to uint8
            image_data = self._convert_to_uint8(self._simulated_image)
            
            # Ensure data is contiguous
            image_data = np.ascontiguousarray(image_data)
            
            # Create QImage
            image = QImage(image_data.data, width, height, bytes_per_line, 
                          QImage.Format.Format_RGB888)
            
            # Convert to QPixmap and scale
            pixmap = QPixmap.fromImage(image)
            return pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        return None 
    
    def get_bands_for_rgb(self, band_numbers):
        """
        Get Band objects for RGB simulation
        Args:
            band_numbers: tuple of 3 integers representing R,G,B band numbers
        Returns:
            tuple of 3 Band objects
        """
        if not self._image_ms:
            raise ValueError("No image loaded")
        
        bands = []
        for number in band_numbers:
            band = self._image_ms.get_band_by_number(number)
            if band is None:
                raise ValueError(f"Band number {number} not found")
            bands.append(band)
        
        return tuple(bands) 
    
    def get_simulation_history(self, sort_by=None, reverse=False):
        """
        Get the simulation history with optional sorting
        Args:
            sort_by (str): Field to sort by ('date', 'image_name', 'simulation_type')
            reverse (bool): Whether to reverse the sort order
        Returns:
            list: Sorted simulation history
        """
        if sort_by:
            return sorted(self._simulation_history, key=lambda x: x[sort_by], reverse=reverse)
        return self._simulation_history
    
    def _get_qimage_from_array(self, image_array):
        """Convert numpy array to QImage"""
        height, width, channels = image_array.shape
        bytes_per_line = channels * width
        
        # Convert to uint8
        image_data = self._convert_to_uint8(image_array)
        
        return QImage(image_data.data, width, height, bytes_per_line, QImage.Format.Format_RGB888) 