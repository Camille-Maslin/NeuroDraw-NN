# NeuroDraw-NN

A educational project implementing a neural network from scratch for digit recognition, designed to understand the fundamentals of neural networks without using complex libraries.

## Description

NeuroDraw-NN is a Python application created for educational purposes to demonstrate how neural networks work at their most basic level. Instead of using sophisticated libraries like TensorFlow or PyTorch, this project implements a simple neural network from scratch, making it easier to understand the core concepts of:

- Forward propagation
- Backpropagation
- Gradient descent
- Activation functions
- Weight and bias adjustments

While this implementation may not be as efficient as professional deep learning libraries, it serves as an excellent learning tool to visualize and understand the inner workings of neural networks.

## Educational Purpose

This project is specifically designed for:
- Students learning about neural networks
- Teaching purposes to visualize how neural networks process data

The code prioritizes readability and understanding over performance, with detailed comments explaining each step of the neural network process.

## Features

- Simple neural network implemented from scratch
- Interactive drawing canvas to test the network
- Visualization of the network's decision-making process
- Detailed documentation of the neural network implementation

## Prerequisites

- Python 3.x
- PyQt5 (for the GUI only)
- NumPy (for basic matrix operations)
- No complex deep learning frameworks required

## Installation

1. Clone the repository:
```bash
git clone https://github.com/camille-maslin/NeuroDraw-NN.git
cd NeuroDraw-NN
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application using:
```bash
python main.py
```

## Project Structure

```bash
NeuroDraw-NN/
├── main.py # Application entry point
├── src/
│ ├── ui/ # User interface components
│ ├── neural_network/ # Neural network implementation
│ │ ├── network.py # Core neural network logic
│ │ ├── activation.py # Activation functions
│ │ └── layer.py # Layer implementation
│ └── utils/ # Helper functions
├── docs/ # Documentation and explanations
├── requirements.txt # Minimal project dependencies
└── README.md # Project documentation
```

## Understanding the Code

The neural network implementation follows these key principles:
1. Simple matrix operations using only NumPy
2. Clear implementation of forward and backward propagation
3. Basic gradient descent optimization
4. Simple activation functions (sigmoid, ReLU)

Example of the network architecture:
- Input layer: 784 neurons (28x28 pixel images)
- Hidden layer: 30 neurons
- Output layer: 10 neurons (digits 0-9)

## Limitations

This project intentionally has certain limitations:
- Not optimized for performance
- Limited to simple network architectures
- Basic implementation of gradient descent
- No advanced features like convolution or regularization

These limitations exist to maintain simplicity and focus on educational value.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
