from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize


class GifButton(QPushButton):

    def __init__(self, gif_path, text, parent=None):
        super().__init__(text, parent)
        # To allow gif icon to appear on button, we need to play it to get its 1st frame
        self.movie = QMovie(gif_path)
        self.movie.start()
        self.setIconSize(QSize(20, 20))
        self.setContentsMargins(0, 0, 0, 0)
        self.setIcon(QIcon(self.movie.currentPixmap()))
        self.movie.stop()
        self.style()
    
    def enterEvent(self, event):
        '''Play gif when mouse enters the button'''
        
        self.movie.frameChanged.connect(self.updateIcon)
        self.movie.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        '''Stop gif when mouse leaves the button'''

        self.movie.frameChanged.disconnect(self.updateIcon)
        self.movie.stop()
        super().leaveEvent(event)
    
    def updateIcon(self):
        self.setIcon(QIcon(self.movie.currentPixmap()))

    def style(self):
        self.setStyleSheet('''
            font-size: 20px;
            margin: 4px, 4px;
        ''')