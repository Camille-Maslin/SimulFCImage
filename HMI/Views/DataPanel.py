from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt

class DataPanel(QWidget):
    """
    Panneau d'affichage des données de l'image
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Image Data")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Grille de données
        grid = QGridLayout()
        
        # Labels des données
        self.name_label = QLabel("Name:")
        self.size_label = QLabel("Dimensions:")
        self.bands_label = QLabel("Bands:")
        self.wavelength_label = QLabel("Wavelength:")
        
        # Valeurs des données
        self.name_value = QLabel()
        self.size_value = QLabel()
        self.bands_value = QLabel()
        self.wavelength_value = QLabel()
        
        # Ajout à la grille
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_value, 0, 1)
        grid.addWidget(self.size_label, 1, 0)
        grid.addWidget(self.size_value, 1, 1)
        grid.addWidget(self.bands_label, 2, 0)
        grid.addWidget(self.bands_value, 2, 1)
        grid.addWidget(self.wavelength_label, 3, 0)
        grid.addWidget(self.wavelength_value, 3, 1)
        
        layout.addLayout(grid) 