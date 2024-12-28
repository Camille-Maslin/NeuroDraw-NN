"""
Network visualization component.
Displays the neural network structure and activations.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QLinearGradient, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF
import numpy as np
from src.utils.config import VISUALIZATION_CONFIG

class NetworkVisualizer(QWidget):
    def __init__(self, network):
        super().__init__()
        self.setMinimumSize(900, 500)  # Increase minimum size
        
        # Calculate dimensions and spacing
        self.margin_h = 80   # Increase horizontal margins
        self.margin_v = 40   # Increase vertical margins
        self.layer_spacing = 300  # More space between layers
        self.neuron_spacing = 20  # More space between neurons
        self.neuron_radius = 8    # Slightly larger neurons
        self.output_width = 120   # Wider output bars
        
        # Layer positions (dynamically calculated in paintEvent)
        self.input_x = None
        self.hidden_x = None
        self.output_x = None
        
        self.network = network
        self.predictions = np.zeros(10)
        self.current_input = np.zeros(784)
        
        # Colors
        self.bg_color = QColor(240, 240, 245)
        self.inactive_color = QColor(200, 200, 220)
        self.active_color = QColor(65, 105, 225)
        
        # Probability bar style
        self.probability_style = """
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db,
                    stop:1 #2ecc71
                );
                border-radius: 3px;
            }
        """
        
        # Prediction history for animation
        self.prediction_history = {i: [] for i in range(10)}
        self.max_history_size = VISUALIZATION_CONFIG.get("max_history_size", 1000)  # Default limit
        
        # Colors for different confidence levels
        self.confidence_colors = {
            'high': QColor("#2ecc71"),    # Green for >70%
            'medium': QColor("#3498db"),   # Blue for >40%
            'low': QColor("#95a5a6")      # Gray for the rest
        }
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Light background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Calculate positions based on current size
        w = self.width()
        h = self.height()
        
        # Horizontal layer positions
        self.input_x = self.margin_h + 100  # More space for input
        self.hidden_x = w // 2
        self.output_x = w - self.margin_h - self.output_width - 50
        
        # Available height for neurons
        available_height = h - 2 * self.margin_v
        
        # Layer titles
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(int(self.input_x - 50), 30, "Input")
        painter.drawText(int(self.hidden_x - 50), 30, "Hidden Layer")
        painter.drawText(int(self.output_x - 50), 30, "Output")
        
        # Draw input as a centered 28x28 grid
        grid_size = 140  # Total grid size
        cell_size = grid_size / 28  # Size of each cell
        
        # Calculate for vertical centering
        total_height = h * 0.6  # Available height for neurons
        start_y = (h - grid_size) / 2  # Center vertically
        start_x = self.input_x - grid_size/2  # Center horizontally
        
        # Grid frame with shadow
        shadow_offset = 3
        shadow_color = QColor(0, 0, 0, 30)
        painter.setPen(Qt.NoPen)
        painter.setBrush(shadow_color)
        painter.drawRect(
            int(start_x + shadow_offset),
            int(start_y + shadow_offset),
            grid_size,
            grid_size
        )
        
        # White background for grid
        painter.setBrush(QColor("white"))
        painter.setPen(QPen(QColor("#3498db"), 2))  # Blue border
        painter.drawRect(int(start_x), int(start_y), grid_size, grid_size)
        
        # Grid cells
        for i in range(28):
            for j in range(28):
                idx = i * 28 + j
                x = start_x + j * cell_size
                y = start_y + i * cell_size
                
                # Draw background grid
                if (i + j) % 2 == 0:
                    painter.fillRect(
                        int(x), int(y),
                        int(cell_size), int(cell_size),
                        QColor(248, 249, 250)
                    )
                
                # Draw active pixel
                activation = float(self.current_input[idx])
                if activation > 0:
                    color = QColor(52, 152, 219, int(activation * 255))  # Blue with transparency
                    painter.fillRect(
                        int(x), int(y),
                        int(cell_size), int(cell_size),
                        color
                    )
        
        # Thinner grid lines
        painter.setPen(QPen(QColor(222, 226, 230), 0.5))
        for i in range(29):
            x = start_x + i * cell_size
            y = start_y + i * cell_size
            painter.drawLine(int(x), int(start_y), int(x), int(start_y + grid_size))
            painter.drawLine(int(start_x), int(y), int(start_x + grid_size), int(y))
        
        # Main grid lines (every 7 pixels)
        painter.setPen(QPen(QColor(206, 212, 218), 1))
        for i in range(0, 29, 7):
            x = start_x + i * cell_size
            y = start_y + i * cell_size
            painter.drawLine(int(x), int(start_y), int(x), int(start_y + grid_size))
            painter.drawLine(int(start_x), int(y), int(start_x + grid_size), int(y))
        
        # Important connections
        if self.network.hidden_activations is not None:
            # Find most important active pixels
            active_inputs = np.where(self.current_input > 0.5)[0]
            hidden_activations = self.network.hidden_activations[0]
            top_hidden = np.argsort(hidden_activations)[-5:]  # Top 5 hidden neurons
            
            # Input -> hidden layer connections
            for idx in active_inputs:
                i, j = idx // 28, idx % 28
                in_x = start_x + j * cell_size + cell_size/2
                in_y = start_y + i * cell_size + cell_size/2
                
                for h_idx in top_hidden:
                    hid_y = h * 0.2 + (h * 0.6 * h_idx / (self.network.hidden_size-1))
                    weight = float(self.network.weights1[idx, h_idx])
                    if weight > 0:
                        color = QColor(0, 0, 255, int(abs(weight * 200)))
                    else:
                        color = QColor(255, 0, 0, int(abs(weight * 200)))
                    pen = QPen(color, max(1, int(abs(weight * 3))))
                    painter.setPen(pen)
                    painter.drawLine(int(in_x), int(in_y), int(self.hidden_x), int(hid_y))
            
            # Hidden layer -> output connections
            for h_idx in top_hidden:
                hid_y = h * 0.2 + (h * 0.6 * h_idx / (self.network.hidden_size-1))
                for o_idx in range(self.network.output_size):
                    if float(self.predictions[o_idx]) > 0.1:  # Show only significant outputs
                        out_y = h * 0.2 + (h * 0.6 * o_idx / (self.network.output_size-1))
                        weight = float(self.network.weights2[h_idx, o_idx])
                        if weight > 0:
                            color = QColor(0, 0, 255, int(abs(weight * 200)))
                        else:
                            color = QColor(255, 0, 0, int(abs(weight * 200)))
                        pen = QPen(color, max(1, int(abs(weight * 3))))
                        painter.setPen(pen)
                        painter.drawLine(int(self.hidden_x), int(hid_y), int(self.output_x), int(out_y))
        
        # Hidden neurons
        if self.network.hidden_activations is not None:
            for i in range(self.network.hidden_size):
                y = h * 0.2 + (h * 0.6 * i / (self.network.hidden_size-1))
                activation = float(self.network.hidden_activations[0, i])
                color = QColor(0, 0, 255, int(activation * 255))
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.black)
                painter.drawEllipse(QPointF(self.hidden_x, y), self.neuron_radius/2, self.neuron_radius/2)
        
        # Output neurons with enhanced visualization
        for i in range(self.network.output_size):
            y = h * 0.2 + (h * 0.6 * i / (self.network.output_size-1))
            activation = float(self.predictions[i])
            
            # Main rectangle
            rect_x = self.output_x + 30
            rect_y = y - 12
            rect_width = 100
            rect_height = 24
            
            # Create main rectangle
            main_rect = QRectF(rect_x, rect_y, rect_width, rect_height)
            
            # Background with slight gradient
            background_gradient = QLinearGradient(main_rect.topLeft(), main_rect.bottomLeft())
            background_gradient.setColorAt(0, QColor("#f8f9fa"))
            background_gradient.setColorAt(1, QColor("#e9ecef"))
            painter.setBrush(background_gradient)
            painter.setPen(QPen(QColor("#dee2e6"), 1))
            painter.drawRoundedRect(main_rect, 4, 4)  # Rounded corners
            
            # Progress bar with gradient
            if activation > 0:
                progress_width = int(rect_width * activation)
                progress_rect = QRectF(rect_x, rect_y, progress_width, rect_height)
                
                # Create gradient based on activation level
                gradient = QLinearGradient(progress_rect.topLeft(), progress_rect.bottomLeft())
                
                if activation > 0.8:
                    # Green for very high confidence
                    gradient.setColorAt(0, QColor("#00b894"))
                    gradient.setColorAt(1, QColor("#00cec9"))
                elif activation > 0.5:
                    # Blue for medium-high confidence
                    gradient.setColorAt(0, QColor("#0984e3"))
                    gradient.setColorAt(1, QColor("#74b9ff"))
                elif activation > 0.3:
                    # Orange for medium-low confidence
                    gradient.setColorAt(0, QColor("#fdcb6e"))
                    gradient.setColorAt(1, QColor("#ffeaa7"))
                else:
                    # Gray for low confidence
                    gradient.setColorAt(0, QColor("#b2bec3"))
                    gradient.setColorAt(1, QColor("#dfe6e9"))
                
                painter.setBrush(gradient)
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(progress_rect, 4, 4)
            
            # Draw digit and percentage
            painter.setPen(Qt.black)
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            
            # Digit on the left
            digit_text = str(i)
            painter.drawText(
                int(rect_x - 25),
                int(rect_y + rect_height/2 + 5),
                digit_text
            )
            
            # Percentage on the right
            percentage = f"{int(activation * 100)}%"
            painter.drawText(
                int(rect_x + rect_width + 5),
                int(rect_y + rect_height/2 + 5),
                percentage
            )
    
    def update_predictions(self, input_image, predictions):
        """Update the network visualization with new predictions"""
        self.current_input = input_image.flatten()
        self.predictions = predictions.flatten()
        
        # Update prediction history
        for i, pred in enumerate(predictions):
            self.prediction_history[i].append(float(pred))
            if len(self.prediction_history[i]) > self.max_history_size:
                self.prediction_history[i].pop(0)
        
        self.update() 