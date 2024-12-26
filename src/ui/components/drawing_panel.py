"""
Drawing panel component for the application.
Handles user drawing input and visualization.
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect
import numpy as np
from PyQt5.QtCore import pyqtSignal
from src.ui.components.drawing_history import DrawingHistory
from src.utils.config import DRAWING_CONFIG

class DrawingPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # Center all content
        
        # Canvas container with border and shadow
        canvas_container = QFrame()
        canvas_container.setStyleSheet("""
            QFrame {
                background-color: #000;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
            }
        """)
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(10, 10, 10, 10)
        
        # Canvas
        self.canvas = Canvas()
        canvas_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        layout.addWidget(canvas_container)
        
        # Controls container
        controls_container = QFrame()
        controls_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton {
                min-width: 100px;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                color: white;
            }
            QPushButton#clear {
                background-color: #2ecc71;
            }
            QPushButton#clear:hover {
                background-color: #27ae60;
            }
            QPushButton#undo, QPushButton#redo {
                background-color: #95a5a6;
            }
            QPushButton#undo:hover, QPushButton#redo:hover {
                background-color: #7f8c8d;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        # Title
        title = QLabel("Drawing Area (30x30)")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Controls
        controls_layout = QVBoxLayout(controls_container)
        
        controls_title = QLabel("Controls")
        controls_title.setStyleSheet("font-weight: bold;")
        controls_layout.addWidget(controls_title)
        
        buttons_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Clear")
        self.undo_btn = QPushButton("Undo")
        self.redo_btn = QPushButton("Redo")
        
        for btn in [self.clear_btn, self.undo_btn, self.redo_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    min-width: 80px;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            buttons_layout.addWidget(btn)
        
        controls_layout.addLayout(buttons_layout)
        layout.addWidget(controls_container)
        
        # Connections
        self.clear_btn.clicked.connect(self.canvas.clear)
        self.undo_btn.clicked.connect(self.canvas.undo)
        self.redo_btn.clicked.connect(self.canvas.redo)
        
        # Initial button states
        self.update_button_states()
        
        # Connect signals to update button states
        self.canvas.image_updated.connect(self.update_button_states)
    
    def update_button_states(self):
        """Updates the enabled/disabled state of undo/redo buttons"""
        self.undo_btn.setEnabled(self.canvas.history.can_undo())
        self.redo_btn.setEnabled(self.canvas.history.can_redo())

class Canvas(QWidget):
    image_updated = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(280, 280)
        self.last_point = None
        self.drawing = False
        self.points = []
        self.strokes = []  # List of strokes (each stroke is a list of points)
        self.current_stroke = []  # Points of the current stroke
        self.grid_size = 28
        self.cell_size = self.width() / self.grid_size
        self.history = DrawingHistory()
        
        # Set black background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(palette)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.current_stroke = [self.last_point]  # Start a new stroke
            self.update()
    
    def mouseMoveEvent(self, event):
        if self.drawing:
            current_point = event.pos()
            if self.last_point:
                dx = current_point.x() - self.last_point.x()
                dy = current_point.y() - self.last_point.y()
                distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                
                if distance > 5:
                    steps = int(distance / 5)
                    for i in range(1, steps + 1):
                        t = i / steps
                        x = self.last_point.x() + dx * t
                        y = self.last_point.y() + dy * t
                        self.current_stroke.append(QPoint(int(x), int(y)))
                else:
                    self.current_stroke.append(current_point)
                
            self.last_point = current_point
            self.update()
            normalized = self.get_normalized_image()
            self.image_updated.emit(normalized)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            if self.current_stroke:  # Add current stroke to the list of strokes
                self.strokes.append(self.current_stroke)
                self.current_stroke = []
                self.history.add_state(self.strokes)
                normalized = self.get_normalized_image()
                self.image_updated.emit(normalized)
    
    def clear(self):
        """Clears the drawing"""
        self.strokes = []
        self.current_stroke = []
        self.history = DrawingHistory()
        self.update()
        empty_image = np.zeros((28, 28), dtype=np.float32)
        self.image_updated.emit(empty_image)
    
    def undo(self):
        strokes = self.history.undo()
        if strokes is not None:
            self.strokes = [stroke.copy() for stroke in strokes]
            self.update()
            normalized = self.get_normalized_image()
            self.image_updated.emit(normalized)
    
    def redo(self):
        strokes = self.history.redo()
        if strokes is not None:
            self.strokes = [stroke.copy() for stroke in strokes]
            self.update()
            normalized = self.get_normalized_image()
            self.image_updated.emit(normalized)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw grid
        pen = QPen(QColor(40, 40, 40))
        pen.setWidth(1)
        painter.setPen(pen)
        
        # More visible grid
        for i in range(self.grid_size):
            x = i * self.cell_size
            y = i * self.cell_size
            painter.drawLine(int(x), 0, int(x), self.height())
            painter.drawLine(0, int(y), self.width(), int(y))
            
            if i % 7 == 0:
                pen.setWidth(2)
                pen.setColor(QColor(60, 60, 60))
                painter.setPen(pen)
                painter.drawLine(int(x), 0, int(x), self.height())
                painter.drawLine(0, int(y), self.width(), int(y))
                pen.setWidth(1)
                pen.setColor(QColor(40, 40, 40))
                painter.setPen(pen)
        
        # Draw frame
        pen = QPen(Qt.white, 2)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width()-1, self.height()-1)
        
        # Draw all completed strokes
        for stroke in self.strokes:
            if stroke:
                pen = QPen()
                pen.setWidth(14)
                pen.setColor(QColor('white'))
                pen.setCapStyle(Qt.RoundCap)
                pen.setJoinStyle(Qt.RoundJoin)
                painter.setPen(pen)
                
                path = QPainterPath()
                path.moveTo(stroke[0])
                for point in stroke[1:]:
                    path.lineTo(point)
                painter.drawPath(path)
                
                # Brilliance effect
                pen.setWidth(10)
                pen.setColor(QColor(220, 220, 255))
                painter.setPen(pen)
                painter.drawPath(path)
        
        # Draw current stroke
        if self.current_stroke:
            pen = QPen()
            pen.setWidth(DRAWING_CONFIG["default_brush_size"])
            pen.setColor(QColor('white'))
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            path = QPainterPath()
            path.moveTo(self.current_stroke[0])
            for point in self.current_stroke[1:]:
                path.lineTo(point)
            painter.drawPath(path)
            
            # Brilliance effect
            pen.setWidth(10)
            pen.setColor(QColor(220, 220, 255))
            painter.setPen(pen)
            painter.drawPath(path)
    
    def get_normalized_image(self):
        """Converts the drawing to a normalized image"""
        # If no strokes have been drawn, return an empty image
        if not self.strokes and not self.current_stroke:
            return np.zeros((28, 28), dtype=np.float32)
        
        image = QImage(28, 28, QImage.Format_Grayscale8)
        image.fill(Qt.black)
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing, False)
        
        # Scale points to 28x28
        scale = 28 / self.width()
        
        # Draw with a thicker pen to better match the MNIST dataset
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor('white'))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        # Draw all completed strokes
        for stroke in self.strokes:
            if stroke:
                scaled_points = []
                for point in stroke:
                    x = int(point.x() * scale)
                    y = int(point.y() * scale)
                    scaled_points.append(QPoint(x, y))
                
                path = QPainterPath()
                path.moveTo(scaled_points[0])
                for point in scaled_points[1:]:
                    path.lineTo(point)
                painter.drawPath(path)
        
        # Draw current stroke
        if self.current_stroke:
            scaled_points = []
            for point in self.current_stroke:
                x = int(point.x() * scale)
                y = int(point.y() * scale)
                scaled_points.append(QPoint(x, y))
            
            path = QPainterPath()
            path.moveTo(scaled_points[0])
            for point in scaled_points[1:]:
                path.lineTo(point)
            painter.drawPath(path)
        
        painter.end()
        
        # Convert to numpy array
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(28, 28)
        
        # Normalize and add slight blur for softening edges
        from scipy.ndimage import gaussian_filter
        normalized = arr.astype(np.float32) / 255.0
        normalized = gaussian_filter(normalized, sigma=0.5)
        
        # Apply higher threshold to eliminate noise
        threshold = 0.15
        normalized[normalized < threshold] = 0.0
        
        # Additional check: if the image is almost empty, consider it empty
        if np.sum(normalized) < 1.0:
            return np.zeros((28, 28), dtype=np.float32)
        
        return normalized 