"""
Style constants for the application.
Contains all the styling information used across the application.
"""

# Colors
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2c3e50"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f1c40f"
ERROR_COLOR = "#e74c3c"
BACKGROUND_COLOR = "#e9ecef"
PANEL_BACKGROUND = "#f8f9fa"

# Font Styles
TITLE_STYLE = """
    font-weight: bold;
    font-size: 18px;
    color: #2c3e50;
    margin-bottom: 15px;
    padding: 5px;
    border-bottom: 2px solid #3498db;
"""

DESCRIPTION_STYLE = """
    color: #34495e;
    font-size: 13px;
    line-height: 1.4;
    margin: 10px 0;
"""

TIPS_STYLE = """
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #4CAF50;
    margin: 10px 0;
    color: #2c3e50;
    font-size: 13px;
"""

# Button Styles
BUTTON_STYLE = """
    QPushButton {
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
        background-color: %s;
        color: white;
    }
    QPushButton:hover {
        background-color: %s;
    }
""" % (PRIMARY_COLOR, SUCCESS_COLOR)

CLOSE_BUTTON_STYLE = """
    QPushButton {
        background-color: transparent;
        color: #666;
        font-size: 24px;
        border: none;
        padding: 10px;
        margin: 5px;
    }
    QPushButton:hover {
        color: #f00;
        background-color: rgba(255, 0, 0, 0.1);
        border-radius: 5px;
    }
"""

# Panel Styles
PANEL_STYLE = """
    QFrame {
        background-color: %s;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #dee2e6;
    }
""" % PANEL_BACKGROUND

# Main Window Style
MAIN_WINDOW_STYLE = """
    QMainWindow {
        background-color: %s;
    }
""" % BACKGROUND_COLOR 