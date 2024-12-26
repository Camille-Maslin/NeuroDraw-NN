from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QLinearGradient, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF
import numpy as np
from src.utils.config import VISUALIZATION_CONFIG

class NetworkVisualizer(QWidget):
    def __init__(self, network):
        super().__init__()
        self.setMinimumSize(900, 500)  # Augmenter la taille minimale
        
        # Calcul des dimensions et espacements
        self.margin_h = 80   # Augmenter les marges horizontales
        self.margin_v = 40   # Augmenter les marges verticales
        self.layer_spacing = 300  # Plus d'espace entre les couches
        self.neuron_spacing = 20  # Plus d'espace entre les neurones
        self.neuron_radius = 8    # Neurones légèrement plus grands
        self.output_width = 120   # Barres de sortie plus larges
        
        # Positions des couches (calculées dynamiquement dans paintEvent)
        self.input_x = None
        self.hidden_x = None
        self.output_x = None
        
        self.network = network
        self.predictions = np.zeros(10)
        self.current_input = np.zeros(784)
        
        # Couleurs
        self.bg_color = QColor(240, 240, 245)
        self.inactive_color = QColor(200, 200, 220)
        self.active_color = QColor(65, 105, 225)
        
        # Style des barres de probabilité
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
        
        # Historique des prédictions pour l'animation
        self.prediction_history = {i: [] for i in range(10)}
        self.max_history_size = VISUALIZATION_CONFIG.get("max_history_size", 1000)  # Limite par défaut
        
        # Couleurs pour les différents niveaux de confiance
        self.confidence_colors = {
            'high': QColor("#2ecc71"),    # Vert pour >70%
            'medium': QColor("#3498db"),   # Bleu pour >40%
            'low': QColor("#95a5a6")      # Gris pour le reste
        }
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fond clair
        painter.fillRect(self.rect(), self.bg_color)
        
        # Calcul des positions en fonction de la taille actuelle
        w = self.width()
        h = self.height()
        
        # Positions horizontales des couches
        self.input_x = self.margin_h + 100  # Plus d'espace pour l'entrée
        self.hidden_x = w // 2
        self.output_x = w - self.margin_h - self.output_width - 50
        
        # Hauteur disponible pour les neurones
        available_height = h - 2 * self.margin_v
        
        # Titres des couches
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(int(self.input_x - 50), 30, "Input")
        painter.drawText(int(self.hidden_x - 50), 30, "Hidden Layer")
        painter.drawText(int(self.output_x - 50), 30, "Output")
        
        # Dessiner l'entrée comme une grille 28x28 centrée
        grid_size = 140  # Taille totale de la grille
        cell_size = grid_size / 28  # Taille de chaque cellule
        
        # Calcul pour centrer verticalement
        total_height = h * 0.6  # Hauteur disponible pour les neurones
        start_y = (h - grid_size) / 2  # Centrer verticalement
        start_x = self.input_x - grid_size/2  # Centrer horizontalement
        
        # Cadre de la grille avec ombre
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
        
        # Fond blanc pour la grille
        painter.setBrush(QColor("white"))
        painter.setPen(QPen(QColor("#3498db"), 2))  # Bordure bleue
        painter.drawRect(int(start_x), int(start_y), grid_size, grid_size)
        
        # Cellules de la grille
        for i in range(28):
            for j in range(28):
                idx = i * 28 + j
                x = start_x + j * cell_size
                y = start_y + i * cell_size
                
                # Dessiner la grille de fond
                if (i + j) % 2 == 0:
                    painter.fillRect(
                        int(x), int(y),
                        int(cell_size), int(cell_size),
                        QColor(248, 249, 250)
                    )
                
                # Dessiner le pixel actif
                activation = self.current_input[idx]
                if activation > 0:
                    color = QColor(52, 152, 219, int(activation * 255))  # Bleu avec transparence
                    painter.fillRect(
                        int(x), int(y),
                        int(cell_size), int(cell_size),
                        color
                    )
        
        # Lignes de la grille plus fines
        painter.setPen(QPen(QColor(222, 226, 230), 0.5))
        for i in range(29):
            x = start_x + i * cell_size
            y = start_y + i * cell_size
            painter.drawLine(int(x), int(start_y), int(x), int(start_y + grid_size))
            painter.drawLine(int(start_x), int(y), int(start_x + grid_size), int(y))
        
        # Lignes principales de la grille (tous les 7 pixels)
        painter.setPen(QPen(QColor(206, 212, 218), 1))
        for i in range(0, 29, 7):
            x = start_x + i * cell_size
            y = start_y + i * cell_size
            painter.drawLine(int(x), int(start_y), int(x), int(start_y + grid_size))
            painter.drawLine(int(start_x), int(y), int(start_x + grid_size), int(y))
        
        # Connexions importantes
        if self.network.hidden_activations is not None:
            # Trouver les pixels actifs les plus importants
            active_inputs = np.where(self.current_input > 0.5)[0]
            hidden_activations = self.network.hidden_activations[0]
            top_hidden = np.argsort(hidden_activations)[-5:]  # Top 5 neurones cachés
            
            # Connexions entrée -> couche cachée
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
            
            # Connexions couche cachée -> sortie
            for h_idx in top_hidden:
                hid_y = h * 0.2 + (h * 0.6 * h_idx / (self.network.hidden_size-1))
                for o_idx in range(self.network.output_size):
                    if self.predictions[o_idx] > 0.1:  # Montrer seulement les sorties significatives
                        out_y = h * 0.2 + (h * 0.6 * o_idx / (self.network.output_size-1))
                        weight = float(self.network.weights2[h_idx, o_idx])
                        if weight > 0:
                            color = QColor(0, 0, 255, int(abs(weight * 200)))
                        else:
                            color = QColor(255, 0, 0, int(abs(weight * 200)))
                        pen = QPen(color, max(1, int(abs(weight * 3))))
                        painter.setPen(pen)
                        painter.drawLine(int(self.hidden_x), int(hid_y), int(self.output_x), int(out_y))
        
        # Neurones cachés
        if self.network.hidden_activations is not None:
            for i in range(self.network.hidden_size):
                y = h * 0.2 + (h * 0.6 * i / (self.network.hidden_size-1))
                activation = float(self.network.hidden_activations[0, i])
                color = QColor(0, 0, 255, int(activation * 255))
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.black)
                painter.drawEllipse(QPointF(self.hidden_x, y), self.neuron_radius/2, self.neuron_radius/2)
        
        # Neurones de sortie avec visualisation améliorée
        for i in range(self.network.output_size):
            y = h * 0.2 + (h * 0.6 * i / (self.network.output_size-1))
            activation = float(self.predictions[i])
            
            # Rectangle principal
            rect_x = self.output_x + 30
            rect_y = y - 12
            rect_width = 100
            rect_height = 24
            
            # Créer le rectangle principal
            main_rect = QRectF(rect_x, rect_y, rect_width, rect_height)
            
            # Fond avec un léger dégradé
            background_gradient = QLinearGradient(main_rect.topLeft(), main_rect.bottomLeft())
            background_gradient.setColorAt(0, QColor("#f8f9fa"))
            background_gradient.setColorAt(1, QColor("#e9ecef"))
            painter.setBrush(background_gradient)
            painter.setPen(QPen(QColor("#dee2e6"), 1))
            painter.drawRoundedRect(main_rect, 4, 4)  # Coins arrondis
            
            # Barre de progression avec dégradé
            if activation > 0:
                progress_width = int(rect_width * activation)
                progress_rect = QRectF(rect_x, rect_y, progress_width, rect_height)
                
                # Créer un dégradé basé sur le niveau d'activation
                gradient = QLinearGradient(progress_rect.topLeft(), progress_rect.bottomLeft())
                
                if activation > 0.8:
                    # Vert pour très haute confiance
                    gradient.setColorAt(0, QColor("#00b894"))
                    gradient.setColorAt(1, QColor("#00cec9"))
                elif activation > 0.5:
                    # Bleu pour confiance moyenne-haute
                    gradient.setColorAt(0, QColor("#0984e3"))
                    gradient.setColorAt(1, QColor("#74b9ff"))
                elif activation > 0.3:
                    # Orange pour confiance moyenne-basse
                    gradient.setColorAt(0, QColor("#fdcb6e"))
                    gradient.setColorAt(1, QColor("#ffeaa7"))
                else:
                    # Rouge pour faible confiance
                    gradient.setColorAt(0, QColor("#d63031"))
                    gradient.setColorAt(1, QColor("#ff7675"))
                
                # Dessiner la barre de progression avec coins arrondis
                path = QPainterPath()
                path.addRoundedRect(progress_rect, 4, 4)
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.NoPen)
                painter.drawPath(path)
                
                # Effet de brillance
                if activation > 0.3:  # Seulement pour les valeurs significatives
                    highlight_path = QPainterPath()
                    highlight_rect = QRectF(rect_x, rect_y, progress_width, rect_height/2)
                    highlight_path.addRoundedRect(highlight_rect, 4, 4)
                    highlight_gradient = QLinearGradient(highlight_rect.topLeft(), highlight_rect.bottomLeft())
                    highlight_gradient.setColorAt(0, QColor(255, 255, 255, 50))
                    highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
                    painter.setBrush(highlight_gradient)
                    painter.drawPath(highlight_path)
            
            # Numéro du chiffre avec cercle
            circle_x = self.output_x - 25
            circle_y = y
            circle_radius = 12
            
            # Cercle de fond
            painter.setBrush(QColor("#f8f9fa"))
            painter.setPen(QPen(QColor("#dee2e6"), 1))
            painter.drawEllipse(QPointF(circle_x, circle_y), circle_radius, circle_radius)
            
            # Numéro
            font = painter.font()
            font.setBold(True)
            font.setPointSize(10)
            painter.setFont(font)
            painter.setPen(QColor("#2d3436"))
            painter.drawText(
                QRectF(circle_x - circle_radius, circle_y - circle_radius, 
                       circle_radius * 2, circle_radius * 2),
                Qt.AlignCenter,
                str(i)
            )
            
            # Pourcentage
            text_color = Qt.white if activation > 0.3 else QColor("#2d3436")
            painter.setPen(text_color)
            font.setPointSize(9)
            painter.setFont(font)
            
            # Calcul de la position du texte
            text_rect = QRectF(rect_x, rect_y, progress_width if activation > 0.3 else rect_width, rect_height)
            painter.drawText(
                text_rect,
                Qt.AlignCenter,
                f"{int(activation * 100)}%"
            )
    
    def update_predictions(self, input_image, predictions):
        """Update network predictions and input visualization"""
        self.current_input = input_image.flatten()
        # S'assurer que predictions est un array 1D de taille 10
        self.predictions = np.array(predictions).flatten()
        
        # Vérifier la taille des prédictions
        if len(self.predictions) != 10:
            print(f"Warning: Unexpected predictions shape: {self.predictions.shape}")
            self.predictions = np.zeros(10)
            return
        
        # Mettre à jour l'historique avec limite
        for i in range(10):
            self.prediction_history[i].append(float(self.predictions[i]))
            if len(self.prediction_history[i]) > self.max_history_size:
                self.prediction_history[i].pop(0)
        
        self.update() 