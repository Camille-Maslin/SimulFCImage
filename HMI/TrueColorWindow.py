import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TrueColorWindow(tk.Toplevel):
    instance = None  # Class variable to track the instance

    def __init__(self, parent, image_path):  # Accept image_path as a parameter
        if TrueColorWindow.instance is not None:
            TrueColorWindow.instance.destroy()  # Close the existing instance
        super().__init__(parent)
        TrueColorWindow.instance = self  # Set the current instance
        self.image_path = image_path  # Store the image_path
        self.title("True Color Simulation")
        self.geometry("800x600")

        # Widgets
        ttk.Label(self, text="True Color Simulation", font=("Arial", 20)).pack(pady=20)
        
        # Create an image label to display the image
        self.image_label = tk.Label(self, text="Display True Color Image Here", font=("Arial", 16))
        self.image_label.pack(pady=20)

        # Simulate Image
        self.simulate_image()

        # Return Home Button
        home_btn = ttk.Button(self, text="Home", command=self.return_home)
        home_btn.pack(pady=10)

    def simulate_image(self):
        # Display the actual image
        img = Image.open(self.image_path)  # Use the image_path passed from MainWindow
        img = img.resize((400, 400))  # Removed Image.ANTIALIAS
        self.img = ImageTk.PhotoImage(img)  # Keep a reference to avoid garbage collection
        self.image_label.config(image=self.img)  # Update the image_label to display the image

    def return_home(self):
        self.destroy()
