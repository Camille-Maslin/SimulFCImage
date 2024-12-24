from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QComboBox, QSpinBox, QMenuBar,
                            QMenu, QMessageBox, QDialog, QTableWidget, QTableWidgetItem,
                            QFrame, QHeaderView, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QImage, QPixmap, QAction, QIcon

from HMI.Views.ImageView import ImageView
from HMI.Views.SimulationPanel import SimulationPanel
from HMI.Views.DataPanel import DataPanel
from HMI.Controllers.MainController import MainController
from ResourceManager import ResourceManager

class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application utilisant PyQt6.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SimulFCImage - Multispectral Image Viewer")
        
        # Initialisation du contrôleur principal
        self.controller = MainController()
        
        # Configuration de l'interface
        self._setup_menu()
        self._setup_ui()
        
        # Load and apply styles
        with open("HMI/Resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())
        
    def _setup_menu(self):
        """Setup the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Import action
        import_action = QAction("Import Image", self)
        import_action.setShortcut("Ctrl+O")
        import_action.triggered.connect(self._import_image)
        file_menu.addAction(import_action)
        
        # Save action
        self.save_action = QAction("Save Simulation", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self._save_simulation)
        self.save_action.setEnabled(False)
        file_menu.addAction(self.save_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # About menu
        about_menu = menubar.addMenu("About")
        
        # Authors action
        authors_action = QAction("Authors", self)
        authors_action.triggered.connect(self._show_about)
        about_menu.addAction(authors_action)
        
    def _import_image(self):
        """Handle image import"""
        try:
            if self.controller.load_image():
                self._update_image_data()
                self._update_image_display()
                # Enable navigation buttons
                self.image_view.prev_button.setEnabled(True)
                self.image_view.next_button.setEnabled(True)
                # Update band spinbox limits
                total_bands = self.controller.get_total_bands()
                self.image_view.update_band_limits(total_bands)
        except Exception as e:
            QMessageBox.warning(self, "Import Error", str(e))
            
    def _save_simulation(self):
        """Handle simulation save"""
        success, error = self.controller.save_simulation()
        if not success:
            QMessageBox.warning(self, "Save Error", error)
            
    def _update_image_data(self):
        """Update image metadata display"""
        data = self.controller.get_image_data()
        if data:
            self.data_panel.name_value.setText(data['name'])
            self.data_panel.size_value.setText(data['size'])
            self.data_panel.bands_value.setText(data['bands'])
            self.data_panel.wavelength_value.setText(data['wavelength'])
            
    def _update_image_display(self):
        """Update the image display"""
        if self.controller.has_image():
            pixmap = self.controller.get_current_band_pixmap()
            if pixmap:
                self.image_view.original_image.setPixmap(pixmap)
                # Update band information
                current_band = self.controller.get_current_band()
                total_bands = self.controller.get_total_bands()
                self.image_view.band_spinbox.setValue(current_band)
                self.image_view.total_bands_label.setText(f"/{total_bands}")
        
    def _setup_ui(self):
        """Configure l'interface utilisateur principale"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal vertical
        main_layout = QVBoxLayout(central_widget)
        
        # Container pour les panneaux supérieurs
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        
        # Panneau de gauche (données et contrôles)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Ajout des composants
        self.data_panel = DataPanel(self.controller)
        self.data_panel.setObjectName("dataPanel")
        self.simulation_panel = SimulationPanel(self.controller, self)
        self.simulation_panel.setObjectName("simulationPanel")
        
        left_layout.addWidget(self.data_panel)
        left_layout.addWidget(self.simulation_panel)
        left_layout.addStretch()
        
        # Panneau central (visualisation des images)
        self.image_view = ImageView(self.controller)
        
        # Ajout des panneaux au layout supérieur
        top_layout.addWidget(left_panel, 1)     # Ratio 1
        top_layout.addWidget(self.image_view, 4) # Ratio 4
        
        # Panneau historique (en bas)
        history_panel = QWidget()
        history_layout = QHBoxLayout(history_panel)
        history_layout.setContentsMargins(10, 5, 10, 5)
        
        # Conteneur des en-têtes à gauche
        headers_container = QWidget()
        headers_layout = QVBoxLayout(headers_container)
        headers_layout.setSpacing(5)
        headers_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Titre de l'historique
        history_title = QLabel("Simulation History")
        history_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        history_title.setProperty("historyTitle", "true")
        headers_layout.addWidget(history_title)
        
        # En-têtes
        headers = [
            {"text": "Generated Image", "sort_key": "date"},
            {"text": "Image name", "sort_key": "image_name"},
            {"text": "Simulation Name", "sort_key": "simulation_type"}
        ]
        
        self.sort_buttons = []
        self.current_sort = {"key": None, "reverse": False}
        
        for header in headers:
            header_container = QWidget()
            header_layout = QHBoxLayout(header_container)
            header_layout.setContentsMargins(0, 0, 0, 0)
            
            label = QPushButton(header["text"])
            label.setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: #666;
                    padding: 5px;
                    text-align: left;
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    color: #333;
                }
            """)
            
            sort_arrow = QLabel("↓")
            sort_arrow.setStyleSheet("color: #666; font-weight: bold;")
            sort_arrow.setVisible(False)
            
            header_layout.addWidget(label)
            header_layout.addWidget(sort_arrow)
            header_layout.addStretch()
            
            # Store button info for sorting
            button_info = {
                "button": label,
                "arrow": sort_arrow,
                "sort_key": header["sort_key"]
            }
            self.sort_buttons.append(button_info)
            
            # Connect button click
            label.clicked.connect(lambda checked, b=button_info: self._handle_sort_click(b))
            
            headers_layout.addWidget(header_container)
        
        # Conteneur pour la liste des simulations
        simulations_scroll = QScrollArea()
        simulations_scroll.setWidgetResizable(True)
        simulations_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        simulations_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        simulations_scroll.setMaximumHeight(120)
        
        simulations_container = QWidget()
        simulations_layout = QHBoxLayout(simulations_container)
        simulations_layout.setSpacing(15)
        simulations_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        simulations_scroll.setWidget(simulations_container)
        
        # Ajout des conteneurs au panneau historique
        history_layout.addWidget(headers_container, 1)
        history_layout.addWidget(simulations_scroll, 5)
        
        # Ajout au layout principal
        main_layout.addWidget(top_container)
        main_layout.addWidget(history_panel)
        
        # Pour les boutons de navigation
        self.image_view.prev_button.setProperty("navigation", "true")
        self.image_view.next_button.setProperty("navigation", "true")
        
        # Pour le spinbox de bande
        self.image_view.band_spinbox.setProperty("bandInfo", "true")
        self.image_view.total_bands_label.setProperty("bandInfo", "true")
        
        # Pour le bouton de sauvegarde
        self.image_view.save_button.setObjectName("saveButton")
        
        # Pour le panneau d'historique
        history_panel.setObjectName("historyPanel")
        history_title.setProperty("historyTitle", "true")
        
        # Ajout du bouton de fermeture en haut à droite
        close_button = QPushButton("×")  # Utilise le symbole × comme texte
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(30, 30)  # Taille fixe pour le bouton
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton#closeButton {
                background-color: transparent;
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding: 0;
            }
            QPushButton#closeButton:hover {
                background-color: #e74c3c;
                color: white;
            }
        """)
        
        # Créer un widget pour contenir le bouton de fermeture
        top_right = QWidget()
        top_right_layout = QHBoxLayout(top_right)
        top_right_layout.setContentsMargins(0, 0, 5, 0)
        top_right_layout.addWidget(close_button)
        
        # Ajouter le widget au coin supérieur droit
        self.menuBar().setCornerWidget(top_right, Qt.Corner.TopRightCorner)
        
    def _handle_sort_click(self, button_info):
        """Handle sort button click"""
        sort_key = button_info["sort_key"]
        
        # Reset all other arrows
        for btn in self.sort_buttons:
            if btn != button_info:
                btn["arrow"].setVisible(False)
        
        # Toggle sort direction if clicking the same column
        if self.current_sort["key"] == sort_key:
            self.current_sort["reverse"] = not self.current_sort["reverse"]
        else:
            self.current_sort["key"] = sort_key
            self.current_sort["reverse"] = False
        
        # Update arrow
        button_info["arrow"].setVisible(True)
        button_info["arrow"].setText("↑" if self.current_sort["reverse"] else "↓")
        
        # Update history display
        self._update_history()
        
    def _update_history(self):
        """Update the history display"""
        history_data = self.controller.get_simulation_history(
            sort_by=self.current_sort["key"],
            reverse=self.current_sort["reverse"]
        )
        
        # Récupérer le conteneur des simulations
        simulations_container = self.findChild(QScrollArea).widget()
        simulations_layout = simulations_container.layout()
        
        # Nettoyer le layout existant
        while simulations_layout.count():
            item = simulations_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Ajouter les nouvelles entrées
        for entry in history_data:
            # Conteneur pour une entrée
            entry_widget = QWidget()
            entry_layout = QVBoxLayout(entry_widget)
            entry_layout.setSpacing(5)
            
            # Miniature
            pixmap = QPixmap.fromImage(entry['image'])
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            entry_layout.addWidget(image_label)
            
            # Nom de l'image
            name_label = QLabel(entry['image_name'])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setWordWrap(True)
            name_label.setFixedWidth(100)
            entry_layout.addWidget(name_label)
            
            # Type de simulation
            simulation_name = entry['simulation_type']
            if entry['simulation_type'] == ResourceManager.RGB_BANDS:
                rgb_values = [str(band.get_number()) for band in entry['parameters']]
                simulation_name += f"\n(R_{rgb_values[0]}, G_{rgb_values[1]}, B_{rgb_values[2]})"
            elif entry['simulation_type'] == ResourceManager.DALTONIAN:
                simulation_name += f"\n{entry['parameters']}"
            
            sim_label = QLabel(simulation_name)
            sim_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sim_label.setWordWrap(True)
            sim_label.setFixedWidth(100)
            entry_layout.addWidget(sim_label)
            
            # Ajouter l'entrée au layout
            simulations_layout.addWidget(entry_widget)
        
        # Ajouter un stretch à la fin pour aligner à gauche
        simulations_layout.addStretch()
        
    def _show_about(self):
        """Show about dialog"""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About")
        about_dialog.setFixedSize(700, 500)
        about_dialog.setModal(True)
        
        main_layout = QVBoxLayout(about_dialog)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(25, 20, 25, 20)
        
        # Layout horizontal pour le haut de la fenêtre
        top_layout = QHBoxLayout()
        
        # Logo à gauche
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(ResourceManager.IUT_LOGO).scaled(
            150, 75,  # Logo un peu plus petit
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        top_layout.addWidget(logo_label)
        
        # Titres à droite du logo
        titles_layout = QVBoxLayout()
        
        title_label = QLabel("SimulFCImage")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("LaBabaTcheam C1")
        subtitle_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        project_label = QLabel("Student Project - IUT Dijon-Auxerre-Nevers\nDeveloped for ImViA Laboratory")
        project_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        titles_layout.addWidget(title_label)
        titles_layout.addWidget(subtitle_label)
        titles_layout.addWidget(project_label)
        
        top_layout.addLayout(titles_layout)
        main_layout.addLayout(top_layout)
        
        # Ligne de séparation
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #e0e0e0; margin: 10px 0;")
        main_layout.addWidget(line)
        
        # Section auteurs avec layout en grille
        authors_label = QLabel("Authors & Roles")
        authors_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        authors_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin: 5px 0;")
        main_layout.addWidget(authors_label)
        
        # Grille 2x2 pour les auteurs
        authors_grid = QGridLayout()
        authors_grid.setSpacing(10)
        
        authors = [
            ("MASLIN Camille", "Project Manager & Developer"),
            ("GIBRIL Lakhdar", "Lead Developer & Technical Architect"),
            ("MOREAU Alexandre", "Developer & Documentation Manager"),
            ("PARIS Alexis", "Developer & Testing Manager")
        ]
        
        for i, (name, role) in enumerate(authors):
            author_widget = QWidget()
            author_widget.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                }
            """)
            
            author_layout = QVBoxLayout(author_widget)
            author_layout.setContentsMargins(10, 8, 10, 8)
            
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
            
            role_label = QLabel(role)
            role_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
            
            author_layout.addWidget(name_label)
            author_layout.addWidget(role_label)
            
            authors_grid.addWidget(author_widget, i // 2, i % 2)
        
        main_layout.addLayout(authors_grid)
        
        # Description finale
        final_text = (
            "This project was developed as part of our studies at IUT Dijon-Auxerre-Nevers, "
            "in collaboration with the ImViA Laboratory. It aims to provide tools for "
            "manipulating multispectral images and simulating various color perception methods, "
            "including human vision, bee vision, and color blindness simulation."
        )
        
        final_label = QLabel(final_text)
        final_label.setWordWrap(True)
        final_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        final_label.setStyleSheet("font-size: 12px; color: #7f8c8d; margin: 10px 0;")
        main_layout.addWidget(final_label)
        
        # Bouton OK
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 30px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        ok_button.clicked.connect(about_dialog.accept)
        main_layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Centre la fenêtre
        about_dialog.move(
            self.x() + (self.width() - about_dialog.width()) // 2,
            self.y() + (self.height() - about_dialog.height()) // 2
        )
        
        about_dialog.exec()
        
    def _show_history(self):
        """Show simulation history"""
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("Simulation History")
        history_dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(history_dialog)
        
        # Get history from controller
        history_data = self.controller.get_simulation_history()
        
        # Create table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Date", "Image Name", "Simulation Type", "Parameters"])
        
        # Fill table with history data
        table.setRowCount(len(history_data))
        for i, entry in enumerate(history_data):
            table.setItem(i, 0, QTableWidgetItem(entry['date']))
            table.setItem(i, 1, QTableWidgetItem(entry['image_name']))
            table.setItem(i, 2, QTableWidgetItem(entry['simulation_type']))
            table.setItem(i, 3, QTableWidgetItem(str(entry['parameters'])))
        
        # Enable sorting
        table.setSortingEnabled(True)
        
        layout.addWidget(table)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(history_dialog.accept)
        layout.addWidget(close_button)
        
        history_dialog.exec() 