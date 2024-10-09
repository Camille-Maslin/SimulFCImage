import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 

class DaltonismWindow(tk.Toplevel):
    def __init__(self, parent, image_path):  # Accept image_path as a parameter
        super().__init__(parent)
        self.image_path = image_path  # Store the image_path
        self.title("Daltonism Simulation")
        self.geometry("800x600")

        # Make this window modal
        self.grab_set()
          
        self.__create_widgets()
        

    def __create_widgets(self):
        # Create an image label to display the image
        self.image_label = tk.Label(self, text="Display Image Here", font=("Arial", 16))
        self.image_label.pack(pady=20)

        # Daltonism Type Dropdown
        self.daltonism_type = tk.StringVar(self)
        self.daltonism_type.set("Tritanopia")

        ttk.Label(self, text="Select Daltonism Type", font=("Arial", 20)).pack(pady=10)
        options = ["Tritanopia", "Deuteranopia", "Protanopia"]
        ttk.OptionMenu(self, self.daltonism_type, *options).pack(pady=10)

        # Simulate Button
        simulate_btn = ttk.Button(self, text="Simulate", command=self.simulate_daltonism)
        simulate_btn.pack(pady=10)

        # Return Home Button
        home_btn = ttk.Button(self, text="Home", command=self.return_home)
        home_btn.pack(pady=10)
        

    def simulate_daltonism(self):
        try:
            # Load the original image
            img = Image.open(self.image_path) 
            img = img.resize((400, 400))  

            # Apply a simple simulation effect based on the selected type 
            daltonism_type = self.daltonism_type.get()
            if daltonism_type == "Tritanopia":
                img = img.convert("L")  # Convert to grayscale for demonstration
            elif daltonism_type == "Deuteranopia":
                img = img.convert("L")  # Convert to grayscale for demonstration
            elif daltonism_type == "Protanopia":
                img = img.convert("L")  # Convert to grayscale for demonstration

            self.img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img)  # Update the image_label to display the image
            self.image_label.text = ""  
        except Exception as e:
            print(f"Error loading image: {e}") 
            

    def return_home(self):
        self.destroy()
