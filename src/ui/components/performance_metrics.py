from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

class PerformanceMetrics(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        # Créer les métriques
        self.accuracy = self.create_metric("Accuracy", "0.00%")
        self.loss = self.create_metric("Loss", "0.0000")
        self.val_loss = self.create_metric("Validation Loss", "0.0000")
        
        layout.addWidget(self.accuracy)
        layout.addWidget(self.loss)
        layout.addWidget(self.val_loss)
    
    def create_metric(self, title, value):
        container = QFrame()
        container.setFrameStyle(QFrame.Panel | QFrame.Raised)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout(container)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; color: #666;")
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 16px; color: #333;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return container
    
    def update_metrics(self, accuracy, loss, val_loss):
        self.accuracy.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively)[1].setText(f"{accuracy:.2%}")
        self.loss.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively)[1].setText(f"{loss:.4f}")
        self.val_loss.findChild(QLabel, "", Qt.FindChildOption.FindChildrenRecursively)[1].setText(f"{val_loss:.4f}") 