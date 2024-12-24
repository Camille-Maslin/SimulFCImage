from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class ImageView(QWidget):
    """
    Widget pour l'affichage des images originales et simulées
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Images container
        images_container = QWidget()
        images_layout = QHBoxLayout(images_container)
        images_layout.setSpacing(20)  # Espacement entre les images
        images_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrage horizontal
        
        # Original image section
        original_section = QWidget()
        original_layout = QVBoxLayout(original_section)
        original_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrage vertical
        
        # Original image title
        original_title = QLabel("Original Image")
        original_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        original_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        original_layout.addWidget(original_title)
        
        # Original image
        self.original_image = QLabel()
        self.original_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_image.setFixedSize(350, 350)  # Taille fixe réduite
        self.original_image.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                background-color: white;
                padding: 5px;
            }
        """)
        original_layout.addWidget(self.original_image)
        
        # Band navigation
        nav_container = QWidget()
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 5, 0, 5)
        nav_layout.setSpacing(10)  # Espacement entre les éléments
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self._previous_band)
        self.prev_button.setProperty("navigation", "true")
        
        # Ajout du spinbox pour la sélection directe de bande
        self.band_spinbox = QSpinBox()
        self.band_spinbox.setMinimum(1)
        self.band_spinbox.setMaximum(1)  # Sera mis à jour quand une image est chargée
        self.band_spinbox.setEnabled(False)
        self.band_spinbox.valueChanged.connect(self._on_band_selected)
        self.band_spinbox.setFixedWidth(70)
        self.band_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 4px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background: white;
            }
            QSpinBox:hover {
                border-color: #3498db;
            }
            QSpinBox:disabled {
                background: #f5f5f5;
            }
        """)
        
        self.total_bands_label = QLabel("/0")
        
        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self._next_band)
        self.next_button.setProperty("navigation", "true")
        
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.band_spinbox)
        nav_layout.addWidget(self.total_bands_label)
        nav_layout.addWidget(self.next_button)
        
        original_layout.addWidget(nav_container)
        
        # Simulated image section
        simulated_section = QWidget()
        simulated_layout = QVBoxLayout(simulated_section)
        simulated_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrage vertical
        
        # Simulated image title
        simulated_title = QLabel("Simulated Image")
        simulated_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        simulated_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        simulated_layout.addWidget(simulated_title)
        
        # Simulated image
        self.simulated_image = QLabel()
        self.simulated_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.simulated_image.setFixedSize(350, 350)  # Taille fixe réduite
        self.simulated_image.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                background-color: white;
                padding: 5px;
            }
        """)
        simulated_layout.addWidget(self.simulated_image)
        
        # Save button
        self.save_button = QPushButton("Save Simulation")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self._save_simulation)
        self.save_button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                background-color: #2196F3;
                color: white;
                margin-top: 5px;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
            QPushButton:hover:!disabled {
                background-color: #1976D2;
            }
        """)
        simulated_layout.addWidget(self.save_button)
        
        # Add sections to images container
        images_layout.addWidget(original_section)
        images_layout.addWidget(simulated_section)
        
        layout.addWidget(images_container)
        
    def _previous_band(self):
        self.controller.previous_band()
        self.controller.get_current_band_pixmap()
        self._update_band_info()
        
    def _next_band(self):
        self.controller.next_band()
        self.controller.get_current_band_pixmap()
        self._update_band_info()
        
    def _update_band_info(self):
        """Update band information display"""
        current = self.controller.get_current_band()
        total = self.controller.get_total_bands()
        self.band_spinbox.setValue(current)  # Met à jour la valeur du spinbox
        
    def _save_simulation(self):
        """Save the current simulation using the controller"""
        success, error = self.controller.save_simulation()
        if not success and error:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Save Error", error)
        
    def _on_band_selected(self, value):
        """Handle direct band selection"""
        if self.controller.has_image():
            if self.controller.set_current_band(value):
                # Mettre à jour l'affichage
                pixmap = self.controller.get_current_band_pixmap()
                if pixmap:
                    self.original_image.setPixmap(pixmap)

    def update_band_limits(self, total_bands):
        """Update spinbox limits when loading a new image"""
        self.band_spinbox.setMaximum(total_bands)
        self.band_spinbox.setEnabled(True)
        self.total_bands_label.setText(f"/{total_bands}") 