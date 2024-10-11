import tkinter as tk
from tkinter import ttk

class SimulationChoiceWindow(tk.Toplevel):
    """
    SimulationChoiceWindow class which inherit of the tk.Toplevel class, 
    this window will allow to choose a simulation method for the image

    Author :   
    """


    def __init__(self, parent : tk.Tk, image_path : str): 
        """
        Constructor of SimulationChoiceWindow class where we initialize the window parameters
        like the title, the size and widgets   

        args :
            - parent : a parent window which inherit on the tk.Tk class
            - image_path (str) : the image path as a string selected in the MainWindow

        Author : 
        """
        super().__init__(parent)
        self.image_path = image_path  # Store the image_path
        self.title("Select Simulation Method")
        self.geometry("400x300")

        self.__initialize_widgets()

    def __initialize_widgets (self) -> None : 
        # Dropdown for selecting simulation
        self.sim_type = tk.StringVar(self)
        self.sim_type.set("True Color")  # Set "True Color" as the default selection

        sim_options = ["True Color", "False Color", "Daltonism Simulation", "Bee Color Simulation"]
        ttk.Label(self, text="Select a Simulation Method", font=("Arial", 14)).pack(pady=20)
        ttk.OptionMenu(self, self.sim_type, "True Color", *sim_options).pack(pady=10)  # Ensure "True Color" is always displayed

        # Proceed Button
        proceed_btn = ttk.Button(self, text="Proceed", command=self.__proceed)
        proceed_btn.pack(pady=10)

    