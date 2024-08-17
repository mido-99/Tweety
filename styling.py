# Set up base colors
twitter_blue_gradient = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1DA1F2, stop:1 #0A74DA)"
x_black_gradient = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #14171A, stop:1 #31373d)"
x_light_gray_gradient = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #657786, stop:1 #AAB8C2)"
white_gradient = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #E1E8ED)"# Global stylesheet

STYLESHEET = f"""
    /*      #* Global widgets       */ 
    QWidget {{
        background-color: {x_black_gradient};
        color: {white_gradient};
        font-family: Arial, sans-serif;
    }}
    QPushButton {{
        background-color: {twitter_blue_gradient};
        color: {white_gradient};
        border: 2px solid {twitter_blue_gradient};
        border-radius: 10px;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {white_gradient};
        color: {twitter_blue_gradient};
    }}
    QPushButton:pressed {{
        background-color: {x_light_gray_gradient};
        color: {twitter_blue_gradient};
    }}
    QToolButton {{
        background-color: {twitter_blue_gradient};
        color: {white_gradient};
        border: 2px solid {twitter_blue_gradient};
        border-radius: 6px;
        font-size: 18px;
    }}
    QToolButton:hover {{
        background-color: {white_gradient};
        color: {twitter_blue_gradient};
    }}
    QToolButton:pressed {{
        background-color: {x_light_gray_gradient};
        color: {twitter_blue_gradient};
    }}

    QLabel {{
        font-size: 18px;
        background: none;
    }}

    QLineEdit {{
        background-color: {x_black_gradient};
        color: white;
        font-size: 16px;
        border: 1px solid {twitter_blue_gradient};
        border-radius: 4px;
        padding: 1px 4px;
    }}
    QLineEdit:focus {{
        border: 1px solid {white_gradient};
    }}

    QPlainTextEdit {{
        background-color: {x_black_gradient};
        color: white;
        font-size: 16px;
        border: 1px solid {twitter_blue_gradient};
        border-radius: 4px;
        padding: 1px 4px;
    }}
    QPlainTextEdit:focus {{
        border: 1px solid {white_gradient};
    }}

    QStackedWidget {{
        background-color: {x_black_gradient};
    }}

    QMenuBar {{
        background-color: {x_black_gradient};
        color: {white_gradient};
    }}

    QStatusBar {{
        background-color: {x_black_gradient};
        color: {white_gradient};
    }}

    QComboBox {{
        background-color: {x_black_gradient};
        color: white;
        font-size: 16px;
        border: 1px solid {twitter_blue_gradient};
        border-radius: 4px;
    }}
    QComboBox::drop-down {{
        background-color: {twitter_blue_gradient};
    }}
    QComboBox QAbstractItemView {{
        color: white;
    }}

    QScrollBar:vertical {{
        background: {twitter_blue_gradient};
        width: 16px;
        border-radius: 4px;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: {white_gradient};  /* Color of the track above and below the handle */
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: {white_gradient};  /* Color of the track above and below the handle */
    }}

    QCheckBox {{
        color: {white_gradient};
        font-size: 14px;
    }}
    QCheckBox::indicator {{
        background-color: {x_black_gradient};
        border: 2px solid {twitter_blue_gradient};
        width: 20px;
        height: 20px;
        border-radius: 4px;
    }}
    QCheckBox::indicator:checked {{
        background-color: {twitter_blue_gradient};
    }}
    
    QSpinBox {{
        font-size: 18px;
        color: white;
    }}

    QRadioButton {{
        color: {white_gradient};
        font-size: 14px;
    }}
    QRadioButton::indicator {{
        background-color: {x_black_gradient};
        border: 2px solid {twitter_blue_gradient};
        width: 20px;
        height: 20px;
        border-radius: 10px;
    }}
    QRadioButton::indicator:checked {{
        background-color: {twitter_blue_gradient};
    }}

    /*      #* Custom widgets       */
    #stackedWidget #home QPushButton {{
        font-size: 24px;
    }}
    QLabel[objectName*="title"]{{
        font-size: 28px;
        qproperty-alignment: 'AlignCenter';
        background-color: none;
    }}
"""

