import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  # Import PIL for image handling
import matplotlib.pyplot as plt
import matplotlib.image as img 
from Storage.FileManager import FileManager
from HMI.SimulationChoiceWindow import SimulationChoiceWindow  # Ensure this import is present

class MainWindow(tk.Tk):
    """
    Class MainWindow which inherit of the tk.TK class, it will represent the main page of the software
    
    Author :
    """

    def __init__(self) :
        """
        Constructor of the class MainWindow, where you can configure the different widgets and the 
        window parameters.

        Author :  Lakhdar Gibril
        """
        # Calling the parent constructor of the Tk class.
        super().__init__()

        self.title("SimulFCImage - Main Window")
        self.geometry("800x600")
        self.configure(bg='white')

        # Style TTK
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        self.style.configure('TLabel', font=('Arial', 14))

        # Widgets
        self.image_path = None
        self.image_label = None  # Initialize image_label
        self.__initialize_widgets()

        # Display default PNG image
        self.__display_default_image()

    def __initialize_widgets (self) :
        # Creating all the label for the image data
        self.image_data_label = tk.Label(self, text="Image Data", bg="white", font=("Arial", 18))
        self.image_data_label.place(x = 20, y = 10)

        self.image_name_label = tk.Label(self, bg="white",font=("Arial", 12))
        self.image_name_label.place(x = 20, y = 70)

        self.reel_number_label = tk.Label(self, bg="white",font=("Arial", 12))
        self.reel_number_label.place(x = 20, y = 130)

        self.start_wavelength_label = tk.Label(self, bg="white",font=("Arial", 12))
        self.start_wavelength_label.place(x = 20, y = 190)

        self.end_wavelength_label = tk.Label(self, bg="white",font=("Arial", 12))
        self.end_wavelength_label.place(x = 20, y = 250)

        self.image_size_label = tk.Label(self, bg="white",font=("Arial", 12))
        self.image_size_label.place(x = 20, y = 310)

        # Creating label for the image
        self.image_label = tk.Label(self, bg="white")
        self.image_label.place(x = 250, y = 70)
        self.image_label.pack(padx=20,pady=40)

        self.image_sim_label = tk.Label(self,bg="white")
        self.image_sim_label.place(x = 520, y = 70) 
        self.image_sim_label.pack(padx=20,pady=30)
        
        # Creating the Save generated image button
        self.save_btn = ttk.Button(self, text = "Save")
        self.save_btn.pack(padx=20)

        # Import Image Button
        import_btn = ttk.Button(self, text="Import an image", command=self.__import_image)
        import_btn.place(x = 20, y = 370)

        # Select Simulation Button
        self.sim_btn = ttk.Button(self, text="Generate a color image", command=self.__open_simulation_choice, state='disabled')
        self.sim_btn.place(x = 20, y = 430)
        
        self.sim_btn = ttk.Button(self, text=">", command=self.__next_reel)
        self.sim_btn.place(x = 650, y = 300)
        
        self.sim_btn = ttk.Button(self, text="<", command=self.__previous_reel)
        self.sim_btn.place(x = 500, y = 300)

    def __display_default_image(self):
        # Load and display the default PNG image
        png_path = "HMI/assets/no-image.1024x1024.png"  # Path to your PNG image

        # Load and display the PNG image
        img = Image.open(png_path)
        img = img.resize((200, 200))  
        self.img = ImageTk.PhotoImage(img)  # Keep a reference to avoid garbage collection
        self.image_label.config(image=self.img)  # Update the image_label to display the image
        self.image_sim_label.config(image=self.img)

    def __import_image(self):
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

                submit_btn = ttk.Button(dialog, text="Submit", command=lambda: self.on_submit(dialog,start_entry,end_entry,step_entry))
                submit_btn.grid(row=3, columnspan=2, pady=10)

                dialog.transient(self)
                dialog.grab_set()
                self.wait_window(dialog)

            except Exception as e:
                print(f"Error loading image: {e}. line : {e.__traceback__.tb_lineno}")  # Print error message to console
                self.image_label.config(text="Error loading image")  # Update label to show error
        else:
            self.image_label.config(text="No Image")  # Reset label if no image is selected
            self.__display_default_image()  # Display the default PNG image

    def on_submit(self,dialog:tk.Toplevel,start_entry:tk.Entry,end_entry:tk.Entry,step_entry:tk.Entry):
        try:
            start_wavelength = int(start_entry.get())
            end_wavelength = int(end_entry.get())
            wavelength_step = int(step_entry.get())
            dialog.destroy()

            # Continue with the image processing
            self.image_ms = FileManager.Load(self.folder_path,start_wavelength,end_wavelength,wavelength_step)

            # Update the image_label to display the picture
            image = Image.fromarray(self.image_ms.get_actualreel().get_shade_of_grey())
            image = image.resize((200, 200))
            
            self.img = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=self.img, text="")

            # Update the label to show the of the imported image
            self.title(f"SimulFCImage - {self.image_ms.get_name()}")  # Optionally update the window title
            
            # Update the existing labels to show the image data
            self.image_name_label.config(text=f"Image name : {self.image_ms.get_name()}")  # Update the existing label
            self.reel_number_label.config(text=f"Number of reels : {self.image_ms.get_number_reels()}")
            self.start_wavelength_label.config(text=f"Start wavelength : {self.image_ms.get_start_wavelength()}")  
            self.end_wavelength_label.config(text=f"End wavelength : {self.image_ms.get_end_wavelength()}") 
            self.image_size_label.config(text=f"Image size : {self.image_ms.get_size()[0]} x {self.image_ms.get_size()[1]}")
             
            # Enable the simulation buttons
            self.sim_btn.config(state='normal')  # Enable the button after image import
        except ValueError:
            tk.Label(dialog, text="Veuillez entrer des valeurs valides.", fg="red").grid(row=4, columnspan=2)

    def __open_simulation_choice(self):
        if self.image_path != None :  # Ensure there is an image path before opening the window
            SimulationChoiceWindow(self, self.image_path)  # Pass image_path to SimulationChoiceWindow
            
    def __next_reel(self):
        self.image_ms.next_reel()
        image = Image.fromarray(self.image_ms.get_actualreel().get_shade_of_grey())
        image = image.resize((200, 200))
        
        self.img = ImageTk.PhotoImage(image=image)
        self.image_label.config(image=self.img, text="")
        
    def __previous_reel(self):
        self.image_ms.previous_reel()
        image = Image.fromarray(self.image_ms.get_actualreel().get_shade_of_grey())
        image = image.resize((200, 200))
        
        self.img = ImageTk.PhotoImage(image=image)
        self.image_label.config(image=self.img, text="")