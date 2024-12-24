from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QComboBox, QSpinBox, QGridLayout, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from ResourceManager import ResourceManager

class SimulationPanel(QWidget):
    """
    Control panel for simulations
    """
    def __init__(self, controller, main_window):
        super().__init__()
        self.controller = controller
        self.main_window = main_window
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Simulation")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Simulation type
        self.simulation_type = QComboBox()
        self.simulation_type.addItems([
            ResourceManager.RGB_BANDS,
            ResourceManager.TRUE_COLOR,
            ResourceManager.BEE_COLOR,
            ResourceManager.DALTONIAN,
            ResourceManager.HUMAN_CONE
        ])
        self.simulation_type.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                selection-background-color: #e6e6e6;
            }
            QComboBox QAbstractItemView::item {
                padding: 5px;
                min-height: 25px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f0f0f0;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e6e6e6;
            }
        """)
        self.simulation_type.currentTextChanged.connect(self._on_simulation_changed)
        layout.addWidget(self.simulation_type)
        
        # Parameters widget
        self.params_widget = QWidget()
        self.params_layout = QVBoxLayout(self.params_widget)
        layout.addWidget(self.params_widget)
        
        # Simulation button
        self.simulate_button = QPushButton("Simulate")
        self.simulate_button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.simulate_button.clicked.connect(self._on_simulate)
        layout.addWidget(self.simulate_button)
        
        # Initialize with first simulation type
        self._on_simulation_changed(self.simulation_type.currentText())
        
    def _on_simulation_changed(self, simulation_type):
        """Handle simulation type change"""
        # Clear previous parameters
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # If the item is a layout, clear it first
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                item.layout().setParent(None)
            
        # Add parameters based on simulation type
        if simulation_type == ResourceManager.RGB_BANDS:
            self._setup_rgb_params()
        elif simulation_type == ResourceManager.DALTONIAN:
            self._setup_daltonian_params()
            
    def _setup_rgb_params(self):
        """Setup RGB band selection parameters"""
        grid = QGridLayout()
        grid.setSpacing(5)  # Réduit l'espacement
        self.rgb_spinboxes = []
        
        max_bands = self.controller.get_total_bands() if self.controller.has_image() else 9999
        
        for i, color in enumerate(['R', 'G', 'B']):
            label = QLabel(color)
            label.setStyleSheet("font-weight: bold; color: #2c3e50;")
            spinbox = QSpinBox()
            spinbox.setMinimum(1)
            spinbox.setMaximum(max_bands)
            spinbox.setValue(1)
            spinbox.setFixedWidth(60)  # Réduit la largeur des spinboxes
            spinbox.setStyleSheet("""
                QSpinBox {
                    padding: 2px;
                    border: 1px solid #bdc3c7;
                    border-radius: 3px;
                }
                QSpinBox:hover {
                    border-color: #3498db;
                }
            """)
            self.rgb_spinboxes.append(spinbox)
            grid.addWidget(label, 0, i*2)
            grid.addWidget(spinbox, 0, i*2+1)
        
        # Centrer les contrôles
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addStretch()
        container_layout.addLayout(grid)
        container_layout.addStretch()
        
        self.params_layout.addWidget(container)
        
    def _setup_daltonian_params(self):
        """Setup color blindness type selection"""
        self.daltonian_type = QComboBox()
        self.daltonian_type.addItems([
            ResourceManager.DEUTERANOPIA,
            ResourceManager.PROTANOPIA,
            ResourceManager.DEUTERANOMALY,
            ResourceManager.PROTANOMALY,
            ResourceManager.TRITANOPIA,
            ResourceManager.TRITANOMALY,
            ResourceManager.ACHROMATOPSIA
        ])
        self.params_layout.addWidget(self.daltonian_type)
        
    def _on_simulate(self):
        """Handle simulation button click"""
        if not self.controller.has_image():
            QMessageBox.warning(self, "Error", "Please import an image first")
            return
            
        simulation_type = self.simulation_type.currentText()
        params = None
        
        # Get parameters based on simulation type
        if simulation_type == ResourceManager.RGB_BANDS:
            try:
                band_numbers = tuple(spin.value() for spin in self.rgb_spinboxes)
                params = self.controller.get_bands_for_rgb(band_numbers)
            except Exception as e:
                QMessageBox.warning(self, "Parameter Error", str(e))
                return
        elif simulation_type == ResourceManager.DALTONIAN:
            params = self.daltonian_type.currentText()
            
        success, error = self.controller.simulate(simulation_type, params)
        
        if success:
            # Enable save action in main window
            self.main_window.save_action.setEnabled(True)
            self.main_window.image_view.save_button.setEnabled(True)
            # Update simulated image display
            self._update_simulated_image()
            # Update history
            self.main_window._update_history()
        else:
            QMessageBox.warning(self, "Simulation Error", error)
        
    def _update_simulated_image(self):
        """Update the simulated image display"""
        pixmap = self.controller.get_simulated_image_pixmap()
        if pixmap:
            self.main_window.image_view.simulated_image.setPixmap(pixmap) 