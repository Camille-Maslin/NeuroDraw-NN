from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt
from src.core.dataset_loader import DatasetLoader
import os

class DatasetPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Dataset Visualization")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(title)
        
        # Grid to display examples
        grid_layout = QGridLayout()
        self.layout.addLayout(grid_layout)
        
        # Load dataset
        data_folder = os.path.join(os.path.dirname(__file__), 'data')
        self.dataset_loader = DatasetLoader(data_folder)
        
        # Create 10 labels for digits with enhanced style
        self.digit_labels = []
        for i in range(10):
            container = QWidget()
            container_layout = QVBoxLayout(container)
            
            # Label for image
            label = QLabel()
            label.setFixedSize(100, 100)
            label.setStyleSheet("""
                QLabel {
                    border: 2px solid #333;
                    background-color: black;
                    padding: 5px;
                }
            """)
            label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(label)
            
            # Label for number
            num_label = QLabel(str(i))
            num_label.setAlignment(Qt.AlignCenter)
            num_label.setStyleSheet("font-size: 12px; font-weight: bold;")
            container_layout.addWidget(num_label)
            
            row = i // 5
            col = i % 5
            grid_layout.addWidget(container, row, col)
            self.digit_labels.append(label)
            
            # Load and display image
            pixmap = self.dataset_loader.get_digit_image(i)
            if pixmap:
                label.setPixmap(pixmap)
            
            # Add digit number
            num_label = QLabel(str(i))
            num_label.setAlignment(Qt.AlignCenter)
            grid_layout.addWidget(num_label, row+2, col) 