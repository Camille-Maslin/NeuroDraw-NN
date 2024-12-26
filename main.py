"""
Entry point of the NeuroDraw application.
This file initializes and starts the application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import DigitRecognitionApp

def main():
    """Main function to start the application"""
    app = QApplication(sys.argv)
    window = DigitRecognitionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()