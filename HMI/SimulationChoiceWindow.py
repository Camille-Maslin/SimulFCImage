import tkinter as tk
from tkinter import ttk
from LogicLayer import ImageMS 
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from Exceptions.NotExistingBandException import NotExistingBandException
from Exceptions.EmptyRGBException import EmptyRGBException
from LogicLayer.Factory.SimulatorFactory import SimulatorFactory

class SimulationChoiceWindow(tk.Toplevel):
    """
    SimulationChoiceWindow class which inherits from the tk.Toplevel class, 
    this window allows users to choose a simulation method for the image.

    Author : Camille Maslin  
    """

    def __init__(self, parent : tk.Tk, image_ms : ImageMS): 
        """
        Constructor of SimulationChoiceWindow class that initializes window parameters
        such as title, size and widgets.   

        Parameters:
            - parent: parent window which inherits from tk.Tk class
            - image_ms: ImageMS object containing the loaded image data

        Author: Camille Maslin
        """
        super().__init__(parent)
        self.__image_ms = image_ms  # Store the image_path
        self.title("Choose a simulation method")
        self.geometry("1000x800")
        self.configure(bg='white')
        
        # Prevent resizing
        self.resizable(False, False)
        self.__initialize_widgets()

    def __initialize_widgets(self):
        # Main frame
        self.__main_frame = tk.Frame(self, bg="white")
        self.__main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Section Image Data (left side)
        self.__image_data_frame = tk.Frame(self.__main_frame, bg="white")
        self.__image_data_frame.pack(side="left", anchor="nw", padx=(0, 20))

        tk.Label(self.__image_data_frame, text="Image Data", bg="white", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(self.__image_data_frame, text=f"Image Name : {self.__image_ms.get_name()}", bg="white").pack(anchor="w")
        tk.Label(self.__image_data_frame, text=f"Band number : {self.__image_ms.get_number_bands()}", bg="white").pack(anchor="w")
        tk.Label(self.__image_data_frame, text=f"Start wavelength : {self.__image_ms.get_start_wavelength():.2f}", bg="white").pack(anchor="w")
        tk.Label(self.__image_data_frame, text=f"End wavelength : {self.__image_ms.get_end_wavelength():.2f}", bg="white").pack(anchor="w")
        tk.Label(self.__image_data_frame, text=f"Image size : {self.__image_ms.get_size()[0]} x {self.__image_ms.get_size()[1]}", bg="white").pack(anchor="w")

        # Section Simulation Choice
        self.__simulation_frame = tk.Frame(self.__main_frame, bg="white")
        self.__simulation_frame.pack(side="left", anchor="nw", padx=20)

        tk.Label(self.__simulation_frame, text="Simulation choice", bg="white", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        # Radio buttons for simulation methods
        self.__sim_choice = tk.StringVar(value="rgb")
        
        ttk.Radiobutton(self.__simulation_frame, text="True color simulation", 
                       variable=self.__sim_choice, value="true",
                       command=self.__update_rgb_state).pack(anchor="w", pady=5)
        ttk.Radiobutton(self.__simulation_frame, text="Daltonien color simulation", 
                       variable=self.__sim_choice, value="daltonien",
                       command=self.__update_rgb_state).pack(anchor="w", pady=5)
        ttk.Radiobutton(self.__simulation_frame, text="Bee color simulation", 
                       variable=self.__sim_choice, value="bee",
                       command=self.__update_rgb_state).pack(anchor="w", pady=5)
        ttk.Radiobutton(self.__simulation_frame, text="RGB bands choice", 
                       variable=self.__sim_choice, value="rgb",
                       command=self.__update_rgb_state).pack(anchor="w", pady=5)

        # Frame for RGB spinboxes
        self.__rgb_frame = tk.Frame(self.__simulation_frame, bg="white")
        self.__rgb_frame.pack(anchor="w", pady=10)

        # Labels et Spinboxes pour R, G, B
        labels = ["R", "G", "B"]
        self.__rgb_values = []
        self.__rgb_labels = []
        
        for i, label in enumerate(labels):
            lbl = tk.Label(self.__rgb_frame, text=label, bg="white")
            lbl.grid(row=0, column=i*2, padx=5)
            self.__rgb_labels.append(lbl)
            
            spinbox = ttk.Spinbox(self.__rgb_frame, from_=1, to=self.__image_ms.get_number_bands(), width=5)
            spinbox.grid(row=0, column=i*2+1, padx=5)
            self.__rgb_values.append(spinbox)

        # Initialize spinboxes state
        self.__update_rgb_state()

        # Frame for image preview
        self.__preview_frame = tk.Frame(self.__main_frame, bg="white")
        self.__preview_frame.pack(side="left", padx=20)

        # Label for current wavelength
        self.__wavelength_label = tk.Label(self.__preview_frame, 
                                            text=f"{self.__image_ms.get_actualband().get_wavelength()[0]:.2f} nm", 
                                            bg="white")
        self.__wavelength_label.pack(pady=(0, 5))

        # Label "Imported Image"
        tk.Label(self.__preview_frame, text="Imported Image", bg="white", font=("Arial", 12)).pack()

        # Image preview
        image = Image.fromarray(self.__image_ms.get_actualband().get_shade_of_grey())
        image = image.resize((300, 300))
        self.__preview_image = ImageTk.PhotoImage(image)
        self.__preview_label = tk.Label(self.__preview_frame, image=self.__preview_image, bg="white")
        self.__preview_label.pack()

        # Frame for navigation buttons
        nav_frame = tk.Frame(self.__preview_frame, bg="white")
        nav_frame.pack(pady=10)

        # Previous/Next buttons and band number display
        self.__prev_btn = ttk.Button(nav_frame, text="Previous", command=self.__previous_band)
        self.__prev_btn.pack(side=tk.LEFT, padx=10)

        self.__band_number_text = tk.Text(nav_frame, height=1, width=3, bg="white")
        self.__band_number_text.insert("1.0", str(self.__image_ms.get_actualband().get_number()))
        self.__band_number_text.pack(side=tk.LEFT, padx=5)
        self.__band_number_text.bind('<Return>', self.__on_return_pressed)

        tk.Label(nav_frame, text=f"/{self.__image_ms.get_number_bands()}", 
                bg="white").pack(side=tk.LEFT)

        self.__next_btn = ttk.Button(nav_frame, text="Next", command=self.__next_band)
        self.__next_btn.pack(side=tk.LEFT, padx=10)

        # Buttons Proceed and Cancel at the bottom
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side="bottom", pady=20)

        ttk.Button(button_frame, text="Proceed", command=self.__proceed).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=10)

        # Logos at the bottom
        self.__logo_frame = tk.Frame(self, bg="white")
        self.__logo_frame.pack(side="bottom", fill="x", pady=20)

        # Load and display logos
        self.__left_logo = ImageTk.PhotoImage(Image.open("HMI/assets/Logo-iut-dijon-auxerre-nevers.png").resize((150, 80)))
        self.__right_logo = ImageTk.PhotoImage(Image.open("HMI/assets/Logo-laboratoire-ImViA.png").resize((150, 80)))

        tk.Label(self.__logo_frame, image=self.__left_logo, bg="white").pack(side="left", padx=20)
        tk.Label(self.__logo_frame, image=self.__right_logo, bg="white").pack(side="right", padx=20)

    def __proceed(self):
        try:
            simulation_type = self.__sim_choice.get()
            factory = SimulatorFactory.instance()
            
            if simulation_type == "rgb":
                rgb_values = [spin.get().strip() for spin in self.__rgb_values]
                if "" in rgb_values:
                    raise EmptyRGBException("Please specify all RGB values")
                
                r, g, b = map(int, rgb_values)
                bands = (
                    self.__image_ms.get_bands()[r-1],
                    self.__image_ms.get_bands()[g-1],
                    self.__image_ms.get_bands()[b-1]
                )
                
                simulator = factory.create("band_choice", self.__image_ms, bands)
            else:
                simulator = factory.create(simulation_type, self.__image_ms)
            
            # Execute the simulation
            simulated_image = simulator.simulate()
            
            # Display the simulated image in the main window
            self.master.display_simulated_image(simulated_image)
            
            self.destroy()
                
        except EmptyRGBException as exception:
            messagebox.showwarning("Attention", str(exception))
        except ValueError:
            messagebox.showwarning("Attention", "Invalid RGB values. Please enter valid numbers.")
        except IndexError:
            messagebox.showwarning("Attention", "Invalid band number. Please check the entered values.")

    def __next_band(self):
        """Changes to next band in the image sequence"""
        self.__image_ms.next_band()
        self.__update_preview()

    def __previous_band(self):
        """Changes to previous band in the image sequence"""
        self.__image_ms.previous_band()
        self.__update_preview()

    def __update_preview(self):
        """
        Updates the preview image and wavelength label.
        Updates the band number display.
        """
        # Update wavelength label
        self.__wavelength_label.config(
            text=f"{self.__image_ms.get_actualband().get_wavelength()[0]:.2f} nm")
        
        # Update image
        image = Image.fromarray(self.__image_ms.get_actualband().get_shade_of_grey())
        image = image.resize((300, 300))
        self.__preview_image = ImageTk.PhotoImage(image)
        self.__preview_label.config(image=self.__preview_image)
        
        # Update band number
        self.__band_number_text.delete("1.0", tk.END)
        self.__band_number_text.insert("1.0", str(self.__image_ms.get_actualband().get_number()))

    def __on_return_pressed(self, event):
        """
        Handles manual band number entry when Return key is pressed.
        Validates and changes to the entered band number.
        """
        band_number = self.__band_number_text.get("1.0", tk.END).strip()
        try:
            band = int(band_number)
            self.__change_band(band)
        except (TypeError, ValueError):
            messagebox.askokcancel("Input Error", "The band number must be an integer, not a string!")
        finally:
            self.__band_number_text.delete("1.0", tk.END)

    def __change_band(self, band_number: int):
        """
        Allows changing the current band number based on user input.
        Validates if the band number exists before changing.

        Parameters:
            - band_number: integer representing the desired band number
        """
        try:
            if (band_number > self.__image_ms.get_number_bands()) or (band_number < 1):
                raise NotExistingBandException("The band is nonexistant")
            else:
                self.__image_ms.set_actualband(band_number)
                self.__update_preview()
        except NotExistingBandException as exception:
            messagebox.askokcancel("Input Error", exception.__str__())

    def __update_rgb_state(self):
        """
        Updates the state of RGB spinboxes based on the selected simulation method.
        Enables spinboxes only when RGB bands choice is selected.
        Updates labels color to indicate enabled/disabled state.
        """
        state = 'normal' if self.__sim_choice.get() == "rgb" else 'disabled'
        
        # Update spinboxes state
        for spinbox in self.__rgb_values:
            spinbox.config(state=state)
        
        # Update labels color
        for label in self.__rgb_labels:
            label.config(fg='black' if state == 'normal' else 'gray')