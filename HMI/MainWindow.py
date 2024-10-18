import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from Storage.FileManager import FileManager
from HMI.SimulationChoiceWindow import SimulationChoiceWindow
from Exceptions.NotExistingBandException import NotExistingBandException

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

        # Set up the main window properties
        self.title("SimulFCImage - Main Window")
        self.attributes('-fullscreen', True)  # Enable fullscreen mode
        self.configure(bg='white')  # Set background color
        self.columnconfigure(0, weight=1)  # Configure column weight for responsiveness
        self.rowconfigure(0, weight=1)  # Configure row weight for responsiveness

        # Configure TTK styles
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # Set the theme
        self.style.configure('TButton', font=('Arial', 12), padding=10)  # Button style
        self.style.configure('TLabel', font=('Arial', 14))  # Label style

        # Initialize instance variables
        self.image_path = None  # Path to the imported image
        self.image_label = None  # Label to display the image

        # Initialize the user interface widgets
        self.__initialize_widgets()

        # Display a default PNG image at startup
        self.__display_default_image()

    def __initialize_widgets(self):
        """
        Initializes the main interface widgets, including frames, labels, and buttons.
        Sets up the layout for displaying image data and controls for user interaction.
        """
        # Main frame to contain the grid layout
        main_frame = tk.Frame(self, bg="white")
        main_frame.grid(sticky="nsew")

        # Configure grid responsiveness
        main_frame.columnconfigure([0, 1, 2], weight=1)
        main_frame.rowconfigure([0, 1, 2, 3], weight=1)

        # Image Data Section
        image_data_frame = tk.Frame(main_frame, bg="white")
        image_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Labels for displaying image data
        self.image_data_label = tk.Label(image_data_frame, text="Image Data", bg="white", font=("Arial", 18))
        self.image_data_label.pack(anchor="w")

        self.image_name_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.image_name_label.pack(anchor="w")

        self.band_number_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.band_number_label.pack(anchor="w")

        self.start_wavelength_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.start_wavelength_label.pack(anchor="w")

        self.end_wavelength_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.end_wavelength_label.pack(anchor="w")

        self.image_size_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.image_size_label.pack(anchor="w")

        # Labels for current band wavelength and number
        self.band_wavelength_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.band_wavelength_label.pack(anchor="w")

        self.band_current_number_label = tk.Label(image_data_frame, bg="white", font=("Arial", 12))
        self.band_current_number_label.pack(anchor="w")

        # Controls section for importing images and generating simulations
        controls_frame = tk.Frame(main_frame, bg="white")
        controls_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

        import_btn = ttk.Button(controls_frame, text="Import an image", command=self.__import_image)
        import_btn.pack(pady=10)

        self.sim_btn = ttk.Button(controls_frame, text="Generate a color image", command=self.__open_simulation_choice, state='disabled')
        self.sim_btn.pack(pady=10)

        # Image Display Section
        image_display_frame = tk.Frame(main_frame, bg="white")
        image_display_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        # Frame to hold both imported and simulated images side by side
        images_frame = tk.Frame(image_display_frame, bg="white")
        images_frame.pack(pady=(0, 5), fill="both", expand=True)

        # Frame for imported image
        imported_image_frame = tk.Frame(images_frame, bg="white")
        imported_image_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        # Label for the current band wavelength
        self.band_wavelength_label = tk.Label(imported_image_frame, bg="white", font=("Arial", 12))
        self.band_wavelength_label.pack(pady=(5, 5))  # Space below the label

        # Label for "Imported Image"
        self.imported_image_label = tk.Label(imported_image_frame, bg="white", text="Imported Image", font=("Arial", 12))
        self.imported_image_label.pack(pady=(0, 5))  # Space below the label

        # Image label for original image
        self.image_label = tk.Label(imported_image_frame, bg="white")
        self.image_label.pack(padx=10, pady=10)

        # Frame for navigation buttons (Previous/Next)
        navigation_frame = tk.Frame(imported_image_frame, bg="white")
        navigation_frame.pack(pady=(10, 5))  # Space between the image and buttons

        # Previous/Next buttons for band navigation
        self.prev_btn = ttk.Button(navigation_frame, text="Previous", command=self.__previous_band, state='disabled')  # Set to disabled initially
        self.prev_btn.pack(side=tk.LEFT, padx=10)

        # Label and buttons for Current "Band Number"
        self.band_current_number_text = tk.Text(navigation_frame, bg="white", font=("Arial", 12),width=3,height=1, state="disabled")
        self.band_current_number_text.pack(side=tk.LEFT, padx=10)
        self.band_total_number_label = tk.Label(navigation_frame, bg="white", font=("Arial", 12))
        self.band_total_number_label.pack(side=tk.LEFT, padx=10)  

        self.next_btn = ttk.Button(navigation_frame, text="Next", command=self.__next_band, state='disabled')  # Set to disabled initially
        self.next_btn.pack(side=tk.LEFT, padx=10)

        # Frame for simulated image
        simulated_image_frame = tk.Frame(images_frame, bg="white")
        simulated_image_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        # Label for "Simulated Image"
        self.simulated_image_label = tk.Label(simulated_image_frame, bg="white", text="Simulated Image", font=("Arial", 12))
        self.simulated_image_label.pack(pady=(30, 5))  # Space above and below the label

        # Image label for simulated image
        self.image_sim_label = tk.Label(simulated_image_frame, bg="white")
        self.image_sim_label.pack(padx=10, pady=(10, 0))  # Add padding above the generated image

        # Save Button
        self.save_btn = ttk.Button(simulated_image_frame, text="Save", state='disabled')
        self.save_btn.pack(pady=20)  # Place the button under the simulated image

        # Initialize the imported image with a default image
        self.default_image_path = "HMI/assets/no-image.1024x1024.png"  # Path to the default image
        self.img = self.load_image(self.default_image_path, size=(400, 400))  # Load the default image with size 400x400
        self.image_label.config(image=self.img)  # Display the default image

        # Initialize the simulated image with a default image
        self.simulated_image = self.load_image(self.default_image_path, size=(400, 400))  # Load the default image
        self.image_sim_label.config(image=self.simulated_image)  # Display the default image

        # Placeholder for logos
        logo_frame = tk.Frame(main_frame, bg="white")
        logo_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")

        # Left logo placeholder
        self.left_logo_image = self.load_image("HMI/assets/Logo-iut-dijon-auxerre-nevers.png", size=(300, 160))  # Store the image with size 300x160
        self.left_logo = tk.Label(logo_frame, image=self.left_logo_image, bg="white")
        self.left_logo.pack(side=tk.LEFT, padx=(100, 10))

        # Right logo placeholder
        self.right_logo_image = self.load_image("HMI/assets/Logo-laboratoire-ImViA.png", size=(300, 160))  # Store the image with size 300x160
        self.right_logo = tk.Label(logo_frame, image=self.right_logo_image, bg="white")
        self.right_logo.pack(side=tk.RIGHT, padx=(10, 100))

        # Quit button at the top right
        quit_btn = ttk.Button(main_frame, text="Quit", command=self.quit_application)
        quit_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ne")  # Place the button at the top right

    def __display_default_image(self):
        """
        Loads and displays the default PNG image when the application starts or when no image is selected.
        """
        png_path = "HMI/assets/no-image.1024x1024.png"
        img = Image.open(png_path)
        img = img.resize((400, 400))  # Resize to the specified size
        self.img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.img)

    def __import_image(self):
        """
        Opens a dialog to import an image and prompts the user to enter wavelength parameters.
        """
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            try:
                # Create a custom dialog window
                dialog = tk.Toplevel(self)
                dialog.title("Enter the wavelengths")

                tk.Label(dialog, text="Start wavelength:").grid(row=0, column=0, padx=10, pady=5)
                start_entry = tk.Entry(dialog)
                start_entry.grid(row=0, column=1, padx=10, pady=5)

                tk.Label(dialog, text="End wavelength:").grid(row=1, column=0, padx=10, pady=5)
                end_entry = tk.Entry(dialog)
                end_entry.grid(row=1, column=1, padx=10, pady=5)

                tk.Label(dialog, text="Wavelength step:").grid(row=2, column=0, padx=10, pady=5)
                step_entry = tk.Entry(dialog)
                step_entry.grid(row=2, column=1, padx=10, pady=5)

                submit_btn = ttk.Button(dialog, text="Submit", command=lambda: self.on_submit(dialog, start_entry, end_entry, step_entry))
                submit_btn.grid(row=3, columnspan=2, pady=10)

                dialog.transient(self)
                dialog.grab_set()
                self.wait_window(dialog)

                self.image_path = self.folder_path  # Update the path of the imported image

            except Exception as e:
                print(f"Error loading image: {e}. line : {e.__traceback__.tb_lineno}")  # Print error message to console
                self.image_label.config(text="Error loading image")  # Update label to show error


    def on_submit(self, dialog: tk.Toplevel, start_entry: tk.Entry, end_entry: tk.Entry, step_entry: tk.Entry):
        """
        Processes the wavelength parameters entered by the user and updates the image display accordingly.

        Parameters:
        - dialog: The dialog window for entering wavelengths.
        - start_entry: Entry widget for the start wavelength.
        - end_entry: Entry widget for the end wavelength.
        - step_entry: Entry widget for the wavelength step.
        """
        try:
            start_wavelength = int(start_entry.get())
            end_wavelength = int(end_entry.get())
            wavelength_step = int(step_entry.get())
            dialog.destroy()

            # Continue with the image processing
            self.image_ms = FileManager.Load(self.folder_path, start_wavelength, end_wavelength, wavelength_step)

            self.__update_image()

            # Update the simulated image with a default image
            self.simulated_image = self.load_image(self.default_image_path, size=(400, 400))  # Load the default image
            self.image_sim_label.config(image=self.simulated_image)  # Display the default image

            # Update the label to show the name of the imported image
            self.title(f"SimulFCImage - {self.image_ms.get_name()}")

            # Update the existing labels to show the image data
            self.image_name_label.config(text=f"Image name : {self.image_ms.get_name()}")  # Update the existing label
            self.band_number_label.config(text=f"Number of bands : {self.image_ms.get_number_bands()}")
            self.start_wavelength_label.config(text=f"Start wavelength : {self.image_ms.get_start_wavelength()}")
            self.end_wavelength_label.config(text=f"End wavelength : {self.image_ms.get_end_wavelength()}")
            self.image_size_label.config(text=f"Image size : {self.image_ms.get_size()[0]} x {self.image_ms.get_size()[1]}")
            self.band_total_number_label.config(text=f"/ {self.image_ms.get_number_bands()}")
            
            # Enable the simulation buttons
            self.sim_btn.config(state='normal')  # Enable the button after image import
            self.prev_btn.config(state='normal')  # Enable the button after image import
            self.next_btn.config(state='normal')  # Enable the button after image import

            self.band_current_number_text.config(state='normal')
            self.band_current_number_text.bind('<Return>', self.__on_return_pressed)
            
            self.__update_data()

            # Enable the Save button after image generation
            self.save_btn.config(state='normal')  
        except ValueError:
            tk.Label(dialog, text="Please enter valid values.", fg="red").grid(row=4, columnspan=2)

    def __open_simulation_choice(self):
        """
        Opens the simulation choice window if an image has been imported.
        """
        if self.image_path is not None:  # Ensure there is an image path before opening the window
            SimulationChoiceWindow(self, self.image_path)  # Pass image_path to SimulationChoiceWindow
            
    def __next_band(self):
        """
        Advances to the next band and updates the displayed image and data.
        """
        self.image_ms.next_band()
        self.__update_image()
        self.__update_data()

    def __previous_band(self):
        """
        Goes back to the previous band and updates the displayed image and data.
        """
        self.image_ms.previous_band()
        self.__update_image()
        self.__update_data()

    def __update_data(self):
        """
        Updates the labels displaying the current band wavelength and number.
        """
        self.band_wavelength_label.config(text=f"{self.image_ms.get_actualband().get_wavelength()[0]} nm - {self.image_ms.get_actualband().get_wavelength()[1]} nm")
        self.band_current_number_text.delete(1.0, tk.END)
        self.band_current_number_text.insert(tk.END, f"{self.image_ms.get_actualband().get_number()}")
    
    def __update_image(self) : 
        """
        Update the image label due to the band change
        """ 
        image = Image.fromarray(self.image_ms.get_actualband().get_shade_of_grey())
        image = image.resize((400, 400))

        self.img = ImageTk.PhotoImage(image=image)
        self.image_label.config(image=self.img, text="")


    def load_image(self, path, size=(400, 400)):  # Default size
        """
        Loads an image from the specified path and resizes it to the given dimensions.

        Parameters:
        - path: The file path of the image to load.
        - size: A tuple specifying the desired width and height.

        Returns:
        - A PhotoImage object for displaying in a label.
        """
        img = Image.open(path)
        img = img.resize(size)  # Resize to the specified size
        return ImageTk.PhotoImage(img)
    
    def __on_return_pressed(self, event):
        band_number = self.band_current_number_text.get(1.0, tk.END).strip()
        try:
            band = int(band_number)
            self.__change_band(band)
        except (TypeError, ValueError):
            messagebox.askokcancel("Input Error", "The band number must be an integer, not a string!")
        finally:
            self.band_current_number_text.delete(1.0, tk.END)

    def __change_band(self, band_number: int):
        """
        Allow to change reel number with the input of the user
        Author : Lakhdar Gibril
        """
        try:
            if (band_number > self.image_ms.get_number_bands()) or (band_number < 1):
                raise NotExistingBandException("The band is nonexistant")
            else:
                self.image_ms.set_actualband(band_number)
                self.__update_image()
                self.__update_data()
        except NotExistingBandException as exception:
            messagebox.askokcancel("Input Error", exception.__str__())

    def quit_application(self):
        """
        Closes the application.
        """
        self.destroy()  # Close the application
