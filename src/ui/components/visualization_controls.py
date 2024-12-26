from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class VisualizationControls(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Visualization Controls")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Boutons de contrôle
        buttons_layout = QHBoxLayout()
        
        self.weights_btn = QPushButton("Weights")
        self.gradients_btn = QPushButton("Gradients")
        self.activations_btn = QPushButton("Activations")
        
        for btn in [self.weights_btn, self.gradients_btn, self.activations_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout) 