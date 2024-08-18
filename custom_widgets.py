from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize


class GifButton(QPushButton):
    def __init__(self, gif_path, text, parent=None):
        super().__init__(text, parent)
        self.movie = QMovie(gif_path)
        self.movie.frameChanged.connect(self.updateIcon)
        self.movie.start()
        self.style()

    def updateIcon(self):
        self.setIcon(QIcon(self.movie.currentPixmap()))
        self.setIconSize(QSize(20, 20))  # Adjust the size as needed

    def style(self):
        self.setStyleSheet('''
            font-size: 20px;
        ''')