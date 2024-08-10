from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import sys

class TweetyScrapy(QMainWindow):
    
    def __init__(self):
        super(TweetyScrapy, self).__init__()
        uic.loadUi('main.ui', self)
        self.handle_buttons()
        self.setUi()
    
    def setUi(self):
        back_pix = QIcon('icons/back.jpg')
        self.backButton.setIcon(back_pix)
        self.backButton.setIconSize(QSize(40, 40))

    def handle_buttons(self):
        self.pushButton.clicked.connect(self.user_prof_data)
        self.pushButton_2.clicked.connect(self.all_user_posts)

    def user_prof_data(self):
        self.pushButton_2.setStyleSheet('background-color: red;')
    
    def all_user_posts(self):
        self.stackedWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    sys.exit(app.exec_())