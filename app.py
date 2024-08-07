from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys

class TweetyScrapy(QMainWindow):
    
    def __init__(self):
        super(TweetyScrapy, self).__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.user_prof_data)
        
    def user_prof_data(self):
        self.pushButton_2.setStyleSheet('background-color: red;')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    sys.exit(app.exec_())