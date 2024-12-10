import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np

from PIL import Image, ImageTk

from Storage.FileManager import FileManager
from LogicLayer.Factory.SimulatorFactory import SimulatorFactory
from LogicLayer.Factory.CreateSimulating.CreateBandChoiceSimulating import CreateBandChoiceSimulator
from LogicLayer.Factory.CreateSimulating.CreateHumanSimulating import CreateHumanSimulator
from LogicLayer.Factory.CreateSimulating.CreateBeeSimulating import CreateBeeSimulator
from LogicLayer.Factory.CreateSimulating.CreateDaltonianSimulating import CreateDaltonianSimulator
from Exceptions.ErrorMessages import ErrorMessages
from Exceptions.NotExistingBandException import NotExistingBandException
from Exceptions.EmptyRGBException import EmptyRGBException
from ResourceManager import ResourceManager

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
        factory.register(ResourceManager.RGB_BANDS, CreateBandChoiceSimulator())
        factory.register(ResourceManager.TRUE_COLOR, CreateHumanSimulator())
        factory.register(ResourceManager.BEE_COLOR, CreateBeeSimulator())
        factory.register(ResourceManager.DALTONIAN, CreateDaltonianSimulator())


        self.__daltonian_types = [
            "Deuteranopia", 
            "Protanopia", 
            "Deuteranomaly", 
            "Protanomaly", 
            "Tritanopia", 
            "Tritanomaly",
            "Achromatopsia"
        ]

        # Set up the main window properties
        self.title("SimulFCImage - Main Window")
        self.state("zoomed") # Maximize the window
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

        # Initialize the user interface 
        self.__init_data_frames()
        self.__init_menu()
        self.__init_labels_and_texts()
        self.__init_controls()
        self.__init_logos()

        # Display a default PNG image at startup
        self.__display_default_image()

        # Attribute to store the simulated image
        self._simulated_image = None
        self.__simulation_type = None
        
    def __init_menu(self):
        # Create a menu bar
        self.__menu_bar = tk.Menu(self.__menu_frame)  # Set font size for menu bar

        # File menu
        self.__file_menu = tk.Menu(self.__menu_bar, tearoff=0)
        self.__file_menu.add_command(label="Load Image", command=self.__import_image)
        self.__file_menu.add_command(label="Save Simulated Image", command=self.__save_simulated_image, state='disabled')
        self.__menu_bar.add_cascade(label="File", menu=self.__file_menu)

        # Simulation menu
        self.__simulation_menu = tk.Menu(self.__menu_bar, tearoff=0)
        factory = SimulatorFactory.instance()
        for sim_type in factory.simulators:
            self.__simulation_menu.add_command(label=sim_type, command=lambda st=sim_type: self.__create_simulate_control(st))
        self.__menu_bar.add_cascade(label="Simulation", menu=self.__simulation_menu)

        # Attach the menu bar to the frame
        self.config(menu=self.__menu_bar)

    def __create_simulate_control(self,simulation_type):
        if self.__image_ms is not None:
            self.__simulation_type = simulation_type 
            for widget in self.__simulation_frame.winfo_children():
                widget.destroy()

            label = tk.Label(self.__simulation_frame, text=simulation_type, bg=ResourceManager.BACKGROUND_COLOR,font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["title"]))
            label.pack(padx=10,pady=5)

            if simulation_type == ResourceManager.DALTONIAN:
                self.__daltonian_type = ttk.Combobox(
                            self.__simulation_frame,
                            values=self.__daltonian_types,
                            state='readonly',
                            width=15
                        )
                self.__daltonian_type.set(self.__daltonian_types[0])
                self.__daltonian_type.bind('<<ComboboxSelected>>')
                self.__daltonian_type.pack(pady=5)

            elif simulation_type == ResourceManager.RGB_BANDS:
                self.__rgb_frame = tk.Frame(self.__simulation_frame, bg=ResourceManager.BACKGROUND_COLOR)
                self.__rgb_frame.pack(anchor="w", pady=5)

                # Labels and Spinboxes for R, G, B
                labels = ["R", "G", "B"]
                self.__rgb_values = []
                self.__rgb_labels = []
                
                for i, label in enumerate(labels):
                    lbl = tk.Label(self.__rgb_frame, text=label, bg=ResourceManager.BACKGROUND_COLOR)
                    lbl.grid(row=0, column=i*2, padx=5)
                    self.__rgb_labels.append(lbl)
                    
                    spinbox = ttk.Spinbox(self.__rgb_frame, from_=1, to=self.__image_ms.get_number_bands(), width=5)
                    spinbox.grid(row=0, column=i*2+1, padx=5)
                    self.__rgb_values.append(spinbox)
                
            proceed_btn = ttk.Button(self.__simulation_frame, text="Simulate", command=lambda :self.__simulate(simulation_type)) 
            proceed_btn.pack(padx=10)
        else:
            messagebox.showwarning("Warning", ErrorMessages.IMPORT_FIRST)

    def __simulate(self, simulation_type):
        try:
            factory = SimulatorFactory.instance()
            
            if simulation_type == ResourceManager.RGB_BANDS:
                rgb_values = [spin.get().strip() for spin in self.__rgb_values]
                if "" in rgb_values:
                    raise EmptyRGBException(ErrorMessages.ENTER_ALL_RGB_VALUES)
                r, g, b = map(int, rgb_values)
                bands = (
                    self.__image_ms.get_bands()[r-1],
                    self.__image_ms.get_bands()[g-1],
                    self.__image_ms.get_bands()[b-1]
                )
                simulator = factory.create(simulation_type, self.__image_ms, bands)
            elif simulation_type == ResourceManager.DALTONIAN:
                simulator = factory.create(
                    simulation_type, 
                    self.__image_ms,
                    None,
                    daltonian_type=self.__daltonian_type.get()
                )
            else:
                simulator = factory.create(simulation_type, self.__image_ms, None)
            
            # Execute the simulation
            simulated_image = simulator.simulate()
            # Display the simulated image in the main window
            self.__display_simulated_image(simulated_image)
        except (EmptyRGBException,ValueError,IndexError) as exception:
        # Those conditions are used for modifying only the ValueError and IndexError message to make them more understandable
            if exception.__class__.__name__ == ValueError.__name__ :
                exception.args = (ErrorMessages.INVALID_RGB_VALUES,)
            elif exception.__class__.__name__ == IndexError.__name__ :
                exception.args = (ErrorMessages.INVALID_BAND_NUMBER,)
            messagebox.showwarning("Warning", exception.__str__())

    def __init_data_frames(self):
        # Main frame to contain the grid layout
        self.__main_frame = tk.Frame(self, bg=ResourceManager.BACKGROUND_COLOR)
        self.__main_frame.grid(sticky="nsew")

        # Configure grid responsiveness
        self.__main_frame.columnconfigure([0, 1, 2], weight=1)
        self.__main_frame.rowconfigure([0, 1, 2, 3], weight=1)

        # Create a frame for the menu bar
        self.__menu_frame = tk.Frame(self.__main_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__menu_frame.grid(row=0, column=0, columnspan=3, sticky="ew")  # Use grid instead of pack

        # Image Data Section
        self.__image_data_frame = tk.Frame(self.__main_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__image_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Controls section for importing images and generating simulations
        self.__controls_frame = tk.Frame(self.__main_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__controls_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

        # Image Display Section
        self.__image_display_frame = tk.Frame(self.__main_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__image_display_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Frame to hold both imported and simulated images side by side
        self.__images_frame = tk.Frame(self.__image_display_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__images_frame.pack(pady=(0, 5), fill="both", expand=True)

        # Frame for imported image
        self.__imported_image_frame = tk.Frame(self.__images_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__imported_image_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        # Frame for navigation buttons (Previous/Next)
        self.__navigation_frame = tk.Frame(self.__imported_image_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__navigation_frame.pack(pady=(10, 5),side=tk.BOTTOM) 

        # Frame for simulated image
        self.__simulated_image_frame = tk.Frame(self.__images_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__simulated_image_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        # Simulation section for controls
        self.__simulation_frame = tk.Frame(self.__main_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__simulation_frame.grid(row=1, column=0, padx=20, sticky="nw")

        # Placeholder for logos
        self.__logo_frame = tk.Frame(self.__main_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__logo_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")
             
    def __init_labels_and_texts(self):
        # Labels for displaying image data
        self.__image_data_label = tk.Label(self.__image_data_frame, text="Image Data", bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["title"]))
        self.__image_data_label.pack(anchor="w")

        self.__image_name_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__image_name_label.pack(anchor="w")

        self.__band_number_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__band_number_label.pack(anchor="w")

        self.__start_wavelength_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__start_wavelength_label.pack(anchor="w")

        self.__end_wavelength_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__end_wavelength_label.pack(anchor="w")

        self.__image_size_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__image_size_label.pack(anchor="w")

        # Labels for current band wavelength and number
        self.__band_wavelength_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__band_wavelength_label.pack(anchor="w")

        self.__band_current_number_label = tk.Label(self.__image_data_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__band_current_number_label.pack(anchor="w")

        # Label for "Imported Image"
        self.__imported_image_label = tk.Label(self.__imported_image_frame, bg=ResourceManager.BACKGROUND_COLOR, text="Imported Image", font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["title"]))
        self.__imported_image_label.pack(pady=(5, 5))

        # Label for the current band wavelength
        self.__band_wavelength_label = tk.Label(self.__imported_image_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__band_wavelength_label.pack(pady=(0, 5))

        # Image label for original image
        self.__image_label = tk.Label(self.__imported_image_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__image_label.pack(padx=10, pady=10)

        # Label for "Simulated Image"
        self.__simulated_image_label = tk.Label(self.__simulated_image_frame, bg=ResourceManager.BACKGROUND_COLOR, text="Simulated Image", font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["title"]))
        self.__simulated_image_label.pack(pady=(5, 5))  

        # Label for simulation type
        self.__simultaion_type_label = tk.Label(self.__simulated_image_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__simultaion_type_label.pack(pady=(0, 5))

        # Image label for simulated image
        self.__image_sim_label = tk.Label(self.__simulated_image_frame, bg=ResourceManager.BACKGROUND_COLOR)
        self.__image_sim_label.pack(padx=10, pady=(10, 0))  

    def __init_logos(self) : 
        # Left logo placeholder
        self.__left_logo_image = self.__load_image(ResourceManager.IUT_LOGO, size=ResourceManager.LOGO_SIZE)  # Store the image with size 300x160
        self.__left_logo = tk.Label(self.__logo_frame, image=self.__left_logo_image, bg=ResourceManager.BACKGROUND_COLOR)
        self.__left_logo.pack(side=tk.LEFT, padx=(100, 10))

        # Right logo placeholder
        self.__right_logo_image = self.__load_image(ResourceManager.IMVIA_LOGO, size=ResourceManager.LOGO_SIZE)  # Store the image with size 300x160
        self.__right_logo = tk.Label(self.__logo_frame, image=self.__right_logo_image, bg=ResourceManager.BACKGROUND_COLOR)
        self.__right_logo.pack(side=tk.RIGHT, padx=(10, 100))

    def __init_controls(self) :

        # Previous/Next buttons for band navigation
        self.__prev_btn = ttk.Button(self.__navigation_frame, text="Previous", command=self.__previous_band, state='disabled')
        self.__prev_btn.pack(side=tk.LEFT, padx=10)
        
        # Label and buttons for Current "Band Number"
        self.__band_current_number_text = tk.Text(self.__navigation_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]), width=3, height=1, state="disabled")
        self.__band_current_number_text.pack(side=tk.LEFT, padx=10)
        self.__band_total_number_label = tk.Label(self.__navigation_frame, bg=ResourceManager.BACKGROUND_COLOR, font=(ResourceManager.FONT_FAMILY, ResourceManager.FONT_SIZES["normal"]))
        self.__band_total_number_label.pack(side=tk.LEFT, padx=10)
        
        self.__next_btn = ttk.Button(self.__navigation_frame, text="Next", command=self.__next_band, state='disabled')
        self.__next_btn.pack(side=tk.LEFT, padx=10)

    def __display_default_image(self):
        png_path = ResourceManager.DEFAULT_IMAGE
        image = Image.open(png_path)
        image = image.resize(ResourceManager.DEFAULT_IMAGE_SIZE)  # Resize to the specified size
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
                messagebox.showwarning("Warning", ErrorMessages.METADATA_REQUIRED)
        else:
            messagebox.showwarning("Warning", ErrorMessages.IMAGE_REQUIRED)

    def __update_image_label(self):
        self.title(f"SimulFCImage - {self.__image_ms.get_name()}")
        self.__image_name_label.config(text=f"Image name : {self.__image_ms.get_name()}")
        self.__band_number_label.config(text=f"Number of bands : {self.__image_ms.get_number_bands()}")
        self.__start_wavelength_label.config(text=f"Start wavelength : {self.__image_ms.get_start_wavelength():.2f} nm")
        self.__end_wavelength_label.config(text=f"End wavelength : {self.__image_ms.get_end_wavelength():.2f} nm")
        self.__image_size_label.config(text=f"Image size : {self.__image_ms.get_size()[0]} x {self.__image_ms.get_size()[1]}")
        self.__band_total_number_label.config(text=f"/ {self.__image_ms.get_number_bands()}")
    
    def __enable_buttons(self):
        self.__prev_btn.config(state='normal')
        self.__next_btn.config(state='normal')
        self.__band_current_number_text.config(state='normal')
        self.__band_current_number_text.bind('<Return>', self.__on_return_pressed)

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
        image = image.resize(ResourceManager.DEFAULT_IMAGE_SIZE)
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
        except (NotExistingBandException,ValueError) as exception :
            if exception.__class__.__name__ == ValueError.__name__ :
                exception.args = (ErrorMessages.BAND_NUMBER_TYPE,) # Modifying the exception message so it is more understandable
            messagebox.askokcancel("Input Error", exception.__str__())
        finally:
            self.__update_data()
            return "break"

    def __display_simulated_image(self, simulated_image : np.ndarray):
        """
        Displays the simulated image in the main window.
        args:
            simulated_image (np.ndarray): Simulated image to display
        """
        # Convert numpy array to PIL image
        image = Image.fromarray((simulated_image * 255).astype(np.uint8))
        image = image.resize(ResourceManager.DEFAULT_IMAGE_SIZE)  # Same size as original image
        
        # Create and update the simulated image in the existing label
        self._simulated_img = ImageTk.PhotoImage(image=image)
        self.__image_sim_label.config(image=self._simulated_img)
        
        # Store the simulated image
        self._simulated_image = simulated_image
        self.__simultaion_type_label.config(text=f"{self.__simulation_type}")
        # Enable the "Save Simulated Image" button
        self.__file_menu.entryconfig("Save Simulated Image", state='normal')


    def __save_simulated_image(self):
        """
        Opens a dialog box to save the simulated image
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[
                ('PNG files','*.png'),
                ('JPEG files','*.jpg'),
                ('TIF files','*.tif'),
                ('All files','*')
            ],
            title='Save Simulated Image'
        )
        
        if file_path:
            FileManager.convert_to_image_and_save(self._simulated_image, file_path) 
    
