"""
Main window of the application.
Contains the main UI layout and initialization.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                           QVBoxLayout, QProgressDialog, QLabel, 
                           QFrame, QPushButton)
from PyQt5.QtCore import Qt
import os
import sys

from src.ui.components.drawing_panel import DrawingPanel
from src.ui.components.network_visualizer import NetworkVisualizer
from src.core.neural_network import SimpleNeuralNetwork
from src.core.dataset_loader import DatasetLoader
from src.ui.styles.style_constants import *
from src.utils.config import *

class DigitRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroDraw - Neural Network Digit Recognition")
        self.showFullScreen()
        self.init_network()
        self.init_ui()
        self.drawing_panel.canvas.image_updated.connect(self.update_prediction)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main widget with margins
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Close button
        quit_button = QPushButton("×")
        quit_button.setStyleSheet(CLOSE_BUTTON_STYLE)
        quit_button.clicked.connect(self.close)
        
        # Top layout for close button
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(quit_button)
        main_layout.addLayout(top_layout)
        
        # Main container
        container = QFrame()
        container.setStyleSheet(PANEL_STYLE)
        main_layout.addWidget(container)
        
        # Horizontal layout for content
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        
        # Left panel (Drawing)
        left_panel = self.create_drawing_panel()
        
        # Right panel (Network Visualization)
        right_panel = self.create_visualization_panel()
        
        # Add panels to main layout
        layout.addWidget(left_panel, 40)   # 40% width
        layout.addWidget(right_panel, 60)  # 60% width
        
        # Set global style
        self.setStyleSheet(MAIN_WINDOW_STYLE)
    
    def create_drawing_panel(self):
        """Create and return the drawing panel"""
        panel = QFrame()
        panel.setStyleSheet(PANEL_STYLE)
        layout = QVBoxLayout(panel)
        
        # Header
        drawing_header = QWidget()
        drawing_header_layout = QVBoxLayout(drawing_header)
        
        title = QLabel("Drawing Area")
        title.setStyleSheet(TITLE_STYLE)
        
        description = QLabel(
            "Draw a digit (0-9)\n"
            "Real-time recognition"
        )
        description.setStyleSheet(DESCRIPTION_STYLE)
        description.setAlignment(Qt.AlignCenter)
        
        drawing_header_layout.addWidget(title)
        drawing_header_layout.addWidget(description)
        layout.addWidget(drawing_header)
        
        # Drawing canvas
        self.drawing_panel = DrawingPanel()
        layout.addWidget(self.drawing_panel)
        
        # Drawing help
        drawing_help = QLabel(
            "Tips:\n"
            "• Grid = Size guide\n"
            "• Draw clearly\n"
            "• Undo/Redo available\n"
            "• Clear to reset"
        )
        drawing_help.setStyleSheet(TIPS_STYLE)
        layout.addWidget(drawing_help)
        
        return panel
    
    def create_visualization_panel(self):
        """Create and return the network visualization panel"""
        panel = QFrame()
        panel.setStyleSheet(PANEL_STYLE)
        layout = QVBoxLayout(panel)
        
        # Header
        viz_header = QWidget()
        viz_header_layout = QVBoxLayout(viz_header)
        
        title = QLabel("Network Visualization")
        title.setStyleSheet(TITLE_STYLE)
        
        description = QLabel(
            "Network Structure:\n"
            "Input (784) → Hidden (28) → Output (10)\n\n"
            "Connections: Blue (+) Red (-)\n"
            "Brightness = Connection Strength"
        )
        description.setStyleSheet(DESCRIPTION_STYLE)
        description.setAlignment(Qt.AlignCenter)
        
        viz_header_layout.addWidget(title)
        viz_header_layout.addWidget(description)
        layout.addWidget(viz_header)
        
        # Network visualization
        self.network_viz = NetworkVisualizer(self.network)
        layout.addWidget(self.network_viz)
        
        # Probability legend
        prob_legend = QLabel(
            "Output bars: Confidence level for each digit"
        )
        prob_legend.setStyleSheet("""
            font-style: italic;
            color: #7f8c8d;
            padding: 10px;
            font-size: 12px;
            text-align: center;
            border-top: 1px solid #ddd;
            margin-top: 10px;
        """)
        prob_legend.setAlignment(Qt.AlignCenter)
        layout.addWidget(prob_legend)
        
        return panel
    
    def init_network(self):
        """Initialize and train the neural network"""
        self.network = SimpleNeuralNetwork()
        
        try:
            self.dataset_loader = DatasetLoader(DATA_DIR)
            self.train_network()
        except Exception as e:
            print(f"Error during initialization: {e}")
    
    def train_network(self):
        """Train the neural network"""
        print("Training network...")
        epochs = TRAINING_CONFIG["epochs"]
        batch_size = TRAINING_CONFIG["batch_size"]
        n_samples = len(self.dataset_loader.train_images)
        total_batches = (n_samples * epochs) // batch_size
        
        progress = QProgressDialog("Training network...", "Cancel", 0, total_batches, self)
        progress.setWindowModality(Qt.WindowModal)
        batch_count = 0
        
        for epoch in range(epochs):
            total_error = 0
            for i in range(0, n_samples, batch_size):
                if progress.wasCanceled():
                    break
                    
                batch_images = self.dataset_loader.train_images[i:i+batch_size]
                batch_labels = self.dataset_loader.train_labels[i:i+batch_size]
                
                for img, label in zip(batch_images, batch_labels):
                    error = self.network.train(img, label)
                    total_error += error
                
                batch_count += 1
                progress.setValue(batch_count)
                
                if i % 1000 == 0:
                    print(f"Epoch {epoch+1}/{epochs}, Batch {i//batch_size}, Error: {total_error/(i+1):.4f}")
        
        progress.close()
        print("Training completed!")
    
    def update_prediction(self, normalized_image):
        """Update network predictions based on drawn image"""
        predictions = self.network.forward(normalized_image)
        self.network_viz.update_predictions(normalized_image, predictions)
    
    def toggleFullScreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self.toggleFullScreen() 