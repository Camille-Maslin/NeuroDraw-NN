import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import struct

class DatasetLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.train_images = None
        self.train_labels = None
        self.test_images = None
        self.test_labels = None
        self.example_images = {}  # Un exemple par chiffre
        self.load_data()
        self.prepare_examples()
    
    def read_idx_images(self, filename):
        """Lit les images au format IDX"""
        with open(filename, 'rb') as f:
            magic, size = struct.unpack(">II", f.read(8))
            nrows, ncols = struct.unpack(">II", f.read(8))
            data = np.frombuffer(f.read(), dtype=np.uint8)
            data = data.reshape(size, nrows, ncols)
            print(f"Image dimensions: {nrows}x{ncols}")  # Afficher les dimensions
            return data
    
    def read_idx_labels(self, filename):
        """Lit les labels au format IDX"""
        with open(filename, 'rb') as f:
            magic, size = struct.unpack(">II", f.read(8))
            data = np.frombuffer(f.read(), dtype=np.uint8)
            return data
    
    def load_data(self):
        """Charge les données depuis les fichiers IDX"""
        try:
            # Chargement des données de test
            test_images_path = f"{self.data_path}/testing/t10k-images.idx3-ubyte"
            test_labels_path = f"{self.data_path}/testing/t10k-labels.idx1-ubyte"
            
            self.test_images = self.read_idx_images(test_images_path)
            self.test_labels = self.read_idx_labels(test_labels_path)
            
            # Essayer de charger les données d'entraînement
            try:
                train_images_path = f"{self.data_path}/training/train-images.idx3-ubyte"
                train_labels_path = f"{self.data_path}/training/train-labels.idx1-ubyte"
                self.train_images = self.read_idx_images(train_images_path)
                self.train_labels = self.read_idx_labels(train_labels_path)
                print("Données d'entraînement chargées avec succès")
            except Exception as e:
                print("Données d'entraînement non trouvées, utilisation des données de test pour l'entraînement")
                self.train_images = self.test_images
                self.train_labels = self.test_labels
            
            # Normaliser les images
            self.train_images = self.train_images.astype('float32') / 255.0
            self.test_images = self.test_images.astype('float32') / 255.0
            
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            raise e
    
    def prepare_examples(self):
        """Prépare un exemple de chaque chiffre"""
        if self.train_images is not None and self.train_labels is not None:
            for digit in range(10):
                # Trouve le premier exemple de chaque chiffre
                idx = np.where(self.train_labels == digit)[0][0]
                self.example_images[digit] = self.train_images[idx]
    
    def get_digit_image(self, digit):
        """Convertit une image numpy en QPixmap"""
        if digit in self.example_images:
            img_data = self.example_images[digit]
            
            # Les données sont déjà en uint8 (0-255)
            
            # Redimensionnement (28x28 -> 100x100)
            from PIL import Image
            img = Image.fromarray(img_data)
            img = img.resize((100, 100))
            img_data = np.array(img)
            
            height, width = img_data.shape
            bytes_per_line = width
            
            qimg = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            return QPixmap.fromImage(qimg)
        return None 