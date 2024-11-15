import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from Storage.FileManager import FileManager
from HMI.SimulationChoiceWindow import SimulationChoiceWindow
from Exceptions.NotExistingBandException import NotExistingBandException
import os
from LogicLayer.Factory.SimulatorFactory import SimulatorFactory
from LogicLayer.Factory.CreateSimulating.CreateBandChoiceSimulating import CreateBandChoiceSimulator
from LogicLayer.Factory.CreateSimulating.CreateHumanSimulating import CreateHumanSimulator
from LogicLayer.Factory.CreateSimulating.CreateBeeSimulating import CreateBeeSimulator
from LogicLayer.Factory.CreateSimulating.CreateDaltonianSimulating import CreateDaltonianSimulator
import numpy as np

class MainWindow(tk.Tk):
    """
    MainWindow class inherits from the Tk class and represents the main interface of the application.
    It provides functionalities to import images, display image data, and generate simulations.
    """

    def __init__(self):
        """
        Initializes the MainWindow class, sets up the window parameters, and initializes the widgets.

        Author :  Camille Maslin, Lakhdar Gibril
        """
        # Calling the parent constructor of the Tk class.
        super().__init__()

        # Initialization of the factory
        factory = SimulatorFactory.instance()
        factory.register("RGB bands choice", CreateBandChoiceSimulator())
        factory.register("True color simulation", CreateHumanSimulator())
        factory.register("Bee color simulation", CreateBeeSimulator())
        factory.register("Daltonian color simulation", CreateDaltonianSimulator())

        # Set up the main window properties
        self.title("SimulFCImage - Main Window")
        self.attributes('-fullscreen', True)  # Enable fullscreen mode
        self.configure(bg='white')  # Set background color
        self.columnconfigure(0, weight=1)  # Configure column weight for responsiveness
        self.rowconfigure(0, weight=1)  # Configure row weight for responsiveness

        # Configure TTK styles
        self.__style = ttk.Style(self)
        self.__style.theme_use('clam')  # Set the theme
        self.__style.configure('TButton', font=('Arial', 12), padding=10)  # Button style
        self.__style.configure('TLabel', font=('Arial', 14))  # Label style

        # Initialize instance variables
        self.__image_label = None  # Label to display the image

        # Initialize to None the ImageMS class object
        self.__image_ms = None

        # Initialize the user interface widgets
        self.__initialize_widgets()
        # Display a default PNG image at startup
        self.__display_default_image()

        # Attribute to store the simulated image
        self._simulated_image = None

    def __initialize_widgets(self):
        """
        Initializes the main interface widgets, including frames, labels, and buttons.
        Sets up the layout for displaying image data and controls for user interaction.
        """
        # Main frame to contain the grid layout
        self.__main_frame = tk.Frame(self, bg="white")
        self.__main_frame.grid(sticky="nsew")

        # Configure grid responsiveness
        self.__main_frame.columnconfigure([0, 1, 2], weight=1)
        self.__main_frame.rowconfigure([0, 1, 2, 3], weight=1)

        # Image Data Section
        self.__image_data_frame = tk.Frame(self.__main_frame, bg="white")
        self.__image_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Labels for displaying image data
        self.__image_data_label = tk.Label(self.__image_data_frame, text="Image Data", bg="white", font=("Arial", 18))
        self.__image_data_label.pack(anchor="w")

        self.__image_name_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__image_name_label.pack(anchor="w")

        self.__band_number_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__band_number_label.pack(anchor="w")

        self.__start_wavelength_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__start_wavelength_label.pack(anchor="w")

        self.__end_wavelength_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__end_wavelength_label.pack(anchor="w")

        self.__image_size_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__image_size_label.pack(anchor="w")

        # Labels for current band wavelength and number
        self.__band_wavelength_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__band_wavelength_label.pack(anchor="w")

        self.__band_current_number_label = tk.Label(self.__image_data_frame, bg="white", font=("Arial", 12))
        self.__band_current_number_label.pack(anchor="w")

        # Controls section for importing images and generating simulations
        self.__controls_frame = tk.Frame(self.__main_frame, bg="white")
        self.__controls_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

        self.__import_btn = ttk.Button(self.__controls_frame, text="Import an image", command=self.__import_image)
        self.__import_btn.pack(pady=10)

        self.__sim_btn = ttk.Button(self.__controls_frame, text="Generate a color image", command=self.__open_simulation_choice, state='disabled')
        self.__sim_btn.pack(pady=10)

        # Image Display Section
        self.__image_display_frame = tk.Frame(self.__main_frame, bg="white")
        self.__image_display_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        # Frame to hold both imported and simulated images side by side
        self.__images_frame = tk.Frame(self.__image_display_frame, bg="white")
        self.__images_frame.pack(pady=(0, 5), fill="both", expand=True)

        # Frame for imported image
        self.__imported_image_frame = tk.Frame(self.__images_frame, bg="white")
        self.__imported_image_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        # Label for the current band wavelength
        self.__band_wavelength_label = tk.Label(self.__imported_image_frame, bg="white", font=("Arial", 12))
        self.__band_wavelength_label.pack(pady=(5, 5))  # Space below the label

        # Label for "Imported Image"
        self.__imported_image_label = tk.Label(self.__imported_image_frame, bg="white", text="Imported Image", font=("Arial", 12))
        self.__imported_image_label.pack(pady=(0, 5))  # Space below the label

        # Image label for original image
        self.__image_label = tk.Label(self.__imported_image_frame, bg="white")
        self.__image_label.pack(padx=10, pady=10)

        # Frame for navigation buttons (Previous/Next)
        self.__navigation_frame = tk.Frame(self.__imported_image_frame, bg="white")
        self.__navigation_frame.pack(pady=(10, 5))  # Space between the image and buttons

        # Previous/Next buttons for band navigation
        self.__prev_btn = ttk.Button(self.__navigation_frame, text="Previous", command=self.__previous_band, state='disabled')  # Set to disabled initially
        self.__prev_btn.pack(side=tk.LEFT, padx=10)

        # Label and buttons for Current "Band Number"
        self.__band_current_number_text = tk.Text(self.__navigation_frame, bg="white", font=("Arial", 12),width=3,height=1, state="disabled")
        self.__band_current_number_text.pack(side=tk.LEFT, padx=10)
        self.__band_total_number_label = tk.Label(self.__navigation_frame, bg="white", font=("Arial", 12))
        self.__band_total_number_label.pack(side=tk.LEFT, padx=10)  

        self.__next_btn = ttk.Button(self.__navigation_frame, text="Next", command=self.__next_band, state='disabled')  # Set to disabled initially
        self.__next_btn.pack(side=tk.LEFT, padx=10)

        # Frame for simulated image
        self.__simulated_image_frame = tk.Frame(self.__images_frame, bg="white")
        self.__simulated_image_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        # Label for "Simulated Image"
        self.__simulated_image_label = tk.Label(self.__simulated_image_frame, bg="white", text="Simulated Image", font=("Arial", 12))
        self.__simulated_image_label.pack(pady=(30, 5))  # Space above and below the label

        # Image label for simulated image
        self.__image_sim_label = tk.Label(self.__simulated_image_frame, bg="white")
        self.__image_sim_label.pack(padx=10, pady=(10, 0))  # Add padding above the generated image

        # Save Button
        self.__save_btn = ttk.Button(self.__simulated_image_frame, text="Save", command=self.__save_simulated_image, state='disabled')
        self.__save_btn.pack(pady=20)  # Place the button under the simulated image

        # Placeholder for logos
        self.__logo_frame = tk.Frame(self.__main_frame, bg="white")
        self.__logo_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")

        # Left logo placeholder
        self.__left_logo_image = self.__load_image("HMI/assets/Logo-iut-dijon-auxerre-nevers.png", size=(300, 160))  # Store the image with size 300x160
        self.__left_logo = tk.Label(self.__logo_frame, image=self.__left_logo_image, bg="white")
        self.__left_logo.pack(side=tk.LEFT, padx=(100, 10))

        # Right logo placeholder
        self.__right_logo_image = self.__load_image("HMI/assets/Logo-laboratoire-ImViA.png", size=(300, 160))  # Store the image with size 300x160
        self.__right_logo = tk.Label(self.__logo_frame, image=self.__right_logo_image, bg="white")
        self.__right_logo.pack(side=tk.RIGHT, padx=(10, 100))

        # Quit button at the top right
        self__quit_btn = ttk.Button(self.__main_frame, text="Quit", command=self.quit_application)
        self__quit_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ne")  # Place the button at the top right

    def __display_default_image(self):
        png_path = "HMI/assets/no-image.1024x1024.png"
        image = Image.open(png_path)
        image = image.resize((400, 400))  # Resize to the specified size
        self.__img = ImageTk.PhotoImage(image)
        self.__image_label.config(image=self.__img)
        self.__image_sim_label.config(image=self.__img)

    def __import_image(self):
        self.__folder_path = filedialog.askopenfilename(
            title="Select the image file",
            filetypes=[("Image Files", "*.tiff;*.tif")]
        )
        
        if self.__folder_path:
            # Ask for the metadata file
            metadata_path = filedialog.askopenfilename(
                title="Select the wavelength metadata file",
                filetypes=[("Text Files", "*.txt")],
                initialdir=os.path.dirname(self.__folder_path)
            )
                
            if metadata_path:
                try:
                    self.__image_ms = FileManager.Load(self.__folder_path, metadata_path)
                    self.__update_image()
                    # Update window title, buttons and labels
                    self.__update_image_label()
                    self.__enable_buttons()    
                    self.__update_data()    
                except Exception as exception :
                    messagebox.showerror("Error", exception.__str__())
            else:
                messagebox.showwarning("Warning", "Metadata file is required. Import cancelled.")
        else:
            messagebox.showwarning("Warning", "Image file is required. Import cancelled.")

    def __update_image_label(self):
        self.title(f"SimulFCImage - {self.__image_ms.get_name()}")
        self.__image_name_label.config(text=f"Image name : {self.__image_ms.get_name()}")
        self.__band_number_label.config(text=f"Number of bands : {self.__image_ms.get_number_bands()}")
        self.__start_wavelength_label.config(text=f"Start wavelength : {self.__image_ms.get_start_wavelength():.2f} nm")
        self.__end_wavelength_label.config(text=f"End wavelength : {self.__image_ms.get_end_wavelength():.2f} nm")
        self.__image_size_label.config(text=f"Image size : {self.__image_ms.get_size()[0]} x {self.__image_ms.get_size()[1]}")
        self.__band_total_number_label.config(text=f"/ {self.__image_ms.get_number_bands()}")
    
    def __enable_buttons(self):
        self.__sim_btn.config(state='normal')
        self.__prev_btn.config(state='normal')
        self.__next_btn.config(state='normal')
        self.__band_current_number_text.config(state='normal')
        self.__band_current_number_text.bind('<Return>', self.__on_return_pressed)
        self.__save_btn.config(state='normal')
    
    def __open_simulation_choice(self):
        if self.__image_ms is not None:
            SimulationChoiceWindow(self, self.__image_ms)
        else:
            messagebox.showwarning("Warning", "Please import an image first.")

    def __next_band(self):
        self.__image_ms.next_band()
        self.__update_image()
        self.__update_data()

    def __previous_band(self):
        self.__image_ms.previous_band()
        self.__update_image()
        self.__update_data()

    def __update_data(self):
        self.__band_wavelength_label.config(text=f"{self.__image_ms.get_actualband().get_wavelength()[0]:.2f} nm")
        self.__band_current_number_text.delete(1.0, tk.END)
        self.__band_current_number_text.insert(tk.END, f"{self.__image_ms.get_actualband().get_number()}")
    
    def __update_image(self) : 
        image = Image.fromarray(self.__image_ms.get_actualband().get_shade_of_grey())
        image = image.resize((400, 400))
        self.__band = ImageTk.PhotoImage(image=image)
        self.__image_label.config(image=self.__band, text="")

    def __load_image(self, path : str, size : tuple = (400, 400)) -> ImageTk.PhotoImage :  # Default size
        img = Image.open(path)
        img = img.resize(size)  # Resize to the specified size
        return ImageTk.PhotoImage(img)
    
    def __on_return_pressed(self, event):
        band_number = self.__band_current_number_text.get(1.0, tk.END).strip()
        try:
            band = int(band_number)
            self.__image_ms.set_actualband(band)
            self.__update_image()
            self.__update_data()
        except (NotExistingBandException,ValueError) as exception :
            if exception.__class__.__name__ == ValueError.__name__ :
                exception.args = ("The band number must be an integer, not a string!",) # Modifying the exception message so it is more understandable
            messagebox.askokcancel("Input Error", exception.__str__())
        finally:
            self.__band_current_number_text.delete(1.0, tk.END)
            
    def quit_application(self):
        self.destroy()  # Close the application

    def display_simulated_image(self, simulated_image : np.ndarray):
        """
        Displays the simulated image in the main window.
        args:
            simulated_image (np.ndarray): Simulated image to display
        """
        # Convert numpy array to PIL image
        image = Image.fromarray((simulated_image * 255).astype(np.uint8))
        image = image.resize((400, 400))  # Same size as original image
        
        # Create and update the simulated image in the existing label
        self._simulated_img = ImageTk.PhotoImage(image=image)
        self.__image_sim_label.config(image=self._simulated_img)
        
        # Store the simulated image and activate the Save button
        self._simulated_image = simulated_image
        self.__save_btn.config(state='normal')

    def __save_simulated_image(self):
        """
        Opens a dialog box to save the simulated image
        """
        file_path = filedialog.asksaveasfilename (
            defaultextension='.png',
            filetypes=[
                ('PNG files','*.png'),
                ('JPEG files','*.jpg'),
                ('TIF files','*.tif'),
                ('All files','*')
            ],
            title='Save Simulated Image'
        )
        FileManager.convert_to_image_and_save(self._simulated_image, file_path) 