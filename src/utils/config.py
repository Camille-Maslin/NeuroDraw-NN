"""
Configuration settings for the application.
Contains all the configurable parameters used across the application.
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
TRAIN_DATA_DIR = os.path.join(DATA_DIR, "train")
TEST_DATA_DIR = os.path.join(DATA_DIR, "testing")

# Neural Network Configuration
NETWORK_CONFIG = {
    "input_size": 784,  # 28x28 pixels
    "hidden_size": 28,
    "output_size": 10,  # 10 digits (0-9)
    "learning_rate": 0.1
}

# Training Parameters
TRAINING_CONFIG = {
    "epochs": 5,
    "batch_size": 32,
    "validation_split": 0.2
}

# UI Configuration
UI_CONFIG = {
    "canvas_size": 280,  # 28x10 pixels
    "grid_size": 28,
    "line_width": 2
}

# Drawing Configuration
DRAWING_CONFIG = {
    "brush_sizes": [2, 5, 10, 15],
    "default_brush_size": 10,
    "default_color": "#000000"
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    "update_interval": 100,  # ms
    "animation_speed": 500,  # ms
    "node_size": 10,
    "edge_width": 1,
    "max_history_size": 1000  # Maximum number of prediction history points to keep
} 