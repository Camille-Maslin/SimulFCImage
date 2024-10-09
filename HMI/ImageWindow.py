import tkinter as tk

class ImageWindow(tk.Toplevel):
    def __init__(self, image_path, simulation_type):
        super().__init__()
        self.title(f"Simulation Result - {simulation_type}")
        self.geometry("800x600")

        # Display area for the image
        self.image_label = tk.Label(self, text=f"Displaying result for: {image_path}")
        self.image_label.pack()

        # Add logic to display the actual image after the simulation is applied
        pass
