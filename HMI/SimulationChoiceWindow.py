import tkinter as tk
from tkinter import ttk
from LogicLayer import ImageMS 

class SimulationChoiceWindow(tk.Toplevel):
    """
    SimulationChoiceWindow class which inherit of the tk.Toplevel class, 
    this window will allow to choose a simulation method for the image

    Author : Camille Maslin  
    """

    def __init__(self, parent : tk.Tk, image_ms : ImageMS): 
        """
        Constructor of SimulationChoiceWindow class where we initialize the window parameters
        like the title, the size and widgets   

        Parameters :
            - parent : a parent window which inherit on the tk.Tk class
            - image_ms : ImageMS object containing the loaded image data

        Author : Camille Maslin
        """
        super().__init__(parent)
        self.__image_ms = image_ms  # Store the image_path
        self.title("Choose a simulation method")
        self.geometry("400x300")

        self.__initialize_widgets()

    def __initialize_widgets(self): 
        # Creating a frame to contain a grid
        self.__frame = tk.Frame(self, bg="white")
        self.__frame.grid(sticky="nsew")

        # Configure columns
        self.__frame.columnconfigure([0, 1, 2, 3], weight=1)
        
        # Configure rows
        self.__frame.rowconfigure([0, 1, 2], weight=1)