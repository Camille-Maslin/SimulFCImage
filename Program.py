import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QIcon
from HMI.Views.MainWindow import MainWindow
from ResourceManager import ResourceManager

def set_light_theme(app):
    """Forces the application to use a light theme"""
    palette = QPalette()
    
    # General background
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(245, 247, 250))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(44, 62, 80))
    
    # Widgets
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(248, 249, 250))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor(44, 62, 80))
    
    # Disabled elements
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(127, 140, 141))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(127, 140, 141))
    
    # Buttons
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(44, 62, 80))
    
    # Selection
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)

if __name__ == "__main__":
    # Create application
    app = QApplication(sys.argv)
    
    # Set application icon
    app.setWindowIcon(QIcon(ResourceManager.APP_LOGO))
    
    # Force Fusion style for better cross-platform consistency
    app.setStyle("Fusion")
    
    # Apply light theme
    set_light_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.setWindowState(Qt.WindowState.WindowFullScreen)
    window.show()
    
    # Run application
    sys.exit(app.exec())
