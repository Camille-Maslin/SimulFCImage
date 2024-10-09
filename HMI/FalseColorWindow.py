import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class FalseColorWindow(tk.Toplevel):
    def __init__(self, parent, image_path):  # Accept image_path as a parameter
        super().__init__(parent)
        self.image_path = image_path  # Store the image_path
        self.title("False Color Simulation")
        self.geometry("800x600")

        # Widgets
        ttk.Label(self, text="False Color Simulation", font=("Arial", 20)).pack(pady=20)
        
        # Create an image label to display the image
        self.image_label = tk.Label(self, text="Display False Color Image Here", font=("Arial", 16))
        self.image_label.pack(pady=20)

        # Simulate Image
        self.simulate_image()

        # Return Home Button
        home_btn = ttk.Button(self, text="Home", command=self.return_home)
        home_btn.pack(pady=10)

    def simulate_image(self):
        # Display the actual image
        img = Image.open(self.image_path)  # Use the image_path passed from MainWindow
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)  # Keep a reference to avoid garbage collection
        self.image_label.config(image=self.img)  # Update the image_label to display the image

    def return_home(self):
        self.destroy()
