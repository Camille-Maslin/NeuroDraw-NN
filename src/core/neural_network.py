import numpy as np

class SimpleNeuralNetwork:
    """
    A simple neural network for digit recognition.
    Architecture: 784 (28x28) input -> 28 hidden -> 10 output neurons
    """
    def __init__(self):
        # Network architecture
        self.input_size = 784  # 28x28 pixels
        self.hidden_size = 28  # Hidden layer neurons
        self.output_size = 10  # Output neurons (digits 0-9)
        
        # Initialize weights using He initialization
        self.weights1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2.0/self.input_size)
        self.weights2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2.0/self.hidden_size)
        
        # Initialize biases
        self.bias1 = np.zeros((1, self.hidden_size))
        self.bias2 = np.zeros((1, self.output_size))
        
        # Store activations for visualization
        self.hidden_activations = None
        self.output_activations = None
        
        self.learning_rate = 0.1
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, x):
        """Forward pass through the network"""
        if len(x.shape) > 1:
            x = x.flatten()
        
        # Vérifier si l'entrée est vide (tous les pixels sont noirs)
        if np.all(x < 0.1):  # Augmenter le seuil ici aussi
            return np.zeros(self.output_size)  # Retourner des probabilités nulles
        
        # Première couche
        hidden = np.dot(x, self.weights1) + self.bias1
        self.hidden_activations = self.sigmoid(hidden)
        
        # Couche de sortie
        output = np.dot(self.hidden_activations, self.weights2) + self.bias2
        self.output_activations = self.sigmoid(output)
        
        # S'assurer que le résultat est un array 1D de taille output_size
        return np.array(self.output_activations).flatten()
    
    def train(self, x, y):
        # Forward pass
        if len(x.shape) > 1:
            x = x.flatten()
        
        # Convertir y en one-hot encoding
        y_true = np.zeros((1, self.output_size))
        y_true[0, y] = 1
        
        # Forward pass
        hidden = np.dot(x, self.weights1) + self.bias1
        hidden_output = self.sigmoid(hidden)
        output = np.dot(hidden_output, self.weights2) + self.bias2
        output_activations = self.sigmoid(output)
        
        # Backward pass
        # Erreur de sortie
        output_error = y_true - output_activations
        output_delta = output_error * self.sigmoid_derivative(output_activations)
        
        # Erreur cachée
        hidden_error = np.dot(output_delta, self.weights2.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(hidden_output)
        
        # Mise à jour des poids
        self.weights2 += self.learning_rate * np.dot(hidden_output.T, output_delta)
        self.bias2 += self.learning_rate * output_delta
        
        self.weights1 += self.learning_rate * np.dot(x.reshape(-1, 1), hidden_delta)
        self.bias1 += self.learning_rate * hidden_delta
        
        return np.mean(np.abs(output_error)) 