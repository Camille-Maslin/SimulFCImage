import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  # Import PIL for image handling
import os
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

        Author :  
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
        self.__create_widgets()

        # Display default PNG image
        self.__display_default_image()


    def __create_widgets (self) :
        self.image_name_label = tk.Label(self, text="No Image Selected", bg="white", font=("Arial", 14))
        self.image_name_label.pack(pady=10)

        self.image_label = tk.Label(self, text="No Image", bg="white", font=("Arial", 12))
        self.image_label.pack()

        # Import Image Button
        import_btn = ttk.Button(self, text="Import Image", command=self.__import_image)
        import_btn.pack(pady=10)

        # Select Simulation Button
        self.sim_btn = ttk.Button(self, text="Select Simulation Method", command=self.__open_simulation_choice, state='disabled')
        self.sim_btn.pack(pady=10)

        # Exit Button
        exit_btn = ttk.Button(self, text="Exit", command=self.quit)
        exit_btn.pack(pady=10)

    def __display_default_image(self):
        # Load and display the default PNG image
        png_path = "HMI/assets/no-image.1024x1024.png"  # Path to your PNG image

        # Load and display the PNG image
        img = Image.open(png_path)
        img = img.resize((400, 400))  # Resize the image
        self.img = ImageTk.PhotoImage(img)  # Keep a reference to avoid garbage collection
        self.image_label.config(image=self.img, text="")  # Update the image_label to display the image

    def __import_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.tiff;*.mat")])
        if self.image_path != None :
            try:
                # Display the image in the MainWindow
                img = Image.open(self.image_path)
                img = img.resize((400, 400))  # Removed Image.ANTIALIAS
                self.img = ImageTk.PhotoImage(img)  # Keep a reference to avoid garbage collection
                
                # Update the image_label to display the image
                self.image_label.config(image=self.img, text="")
                
                # Update the label to show the name of the imported image
                image_name = self.image_path.split("/")[-1]  # Get the file name from the path
                self.title(f"SimulFCImage - {image_name}")  # Optionally update the window title
                
                # Update the existing label to show the image name
                self.image_name_label.config(text=image_name)  # Update the existing label
                
                # Enable the simulation button
                self.sim_btn.config(state='normal')  # Enable the button after image import
            except Exception as e:
                print(f"Error loading image: {e}")  # Print error message to console
                self.image_label.config(text="Error loading image")  # Update label to show error
        else:
            self.image_label.config(text="No Image")  # Reset label if no image is selected
            self.__display_default_image()  # Display the default PNG image

    def __open_simulation_choice(self):
        if self.image_path != None :  # Ensure there is an image path before opening the window
            SimulationChoiceWindow(self, self.image_path)  # Pass image_path to SimulationChoiceWindow
        else:
            print("No image selected to pass to SimulationChoiceWindow.")  # Debugging message

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
