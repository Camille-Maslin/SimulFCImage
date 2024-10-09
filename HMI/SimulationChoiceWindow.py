import tkinter as tk
from tkinter import ttk
from HMI.TrueColorWindow import TrueColorWindow
from HMI.FalseColorWindow import FalseColorWindow
from HMI.DaltonismWindow import DaltonismWindow
from HMI.BeeColorWindow import BeeColorWindow

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

        self.__create_widgets()

    def __create_widgets (self) -> None : 
        # Dropdown for selecting simulation
        self.sim_type = tk.StringVar(self)
        self.sim_type.set("True Color")  # Set "True Color" as the default selection

        sim_options = ["True Color", "False Color", "Daltonism Simulation", "Bee Color Simulation"]
        ttk.Label(self, text="Select a Simulation Method", font=("Arial", 14)).pack(pady=20)
        ttk.OptionMenu(self, self.sim_type, "True Color", *sim_options).pack(pady=10)  # Ensure "True Color" is always displayed

        # Proceed Button
        proceed_btn = ttk.Button(self, text="Proceed", command=self.proceed)
        proceed_btn.pack(pady=10)

    def proceed(self) -> None:
        sim_type = self.sim_type.get()
        print(f"Selected simulation type: {sim_type}")  # Debugging line
        if self.image_path is None:
            print("No image path provided!")  # Debugging line
            return  # Exit if no image path is available
        if sim_type == "True Color":
            print("Opening True Color Window...")  # Debugging line
            TrueColorWindow(self, self.image_path)  # Pass image_path to TrueColorWindow
        elif sim_type == "False Color":
            print("Opening False Color Window...")  # Debugging line
            FalseColorWindow(self, self.image_path)  # Pass image_path to FalseColorWindow
        elif sim_type == "Daltonism Simulation":
            print("Opening Daltonism Window...")  # Debugging line
            DaltonismWindow(self, self.image_path)  # Pass image_path to DaltonismWindow
        elif sim_type == "Bee Color Simulation":
            print("Opening Bee Color Window...")  # Debugging line
            BeeColorWindow(self, self.image_path)  # Pass image_path to BeeColorWindow
