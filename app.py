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
        
        self.backButtons()

    def backButtons(self):
        
        back_pix = QIcon('icons/back.jpg')
        back_btns = [btn for btn in self.findChildren(QPushButton) if 'backButton' in btn.objectName()]

        for btn in back_btns:
            # UI
            btn.setIcon(back_pix)
            btn.setIconSize(QSize(40, 40))
            btn.setGeometry(0, 0, 40, 40)
            # Function
            btn.clicked.connect(self.go_home)
    
    
    def handle_buttons(self):
        self.goto_profile.clicked.connect(self.user_prof_data)
        self.goto_user_tweets.clicked.connect(self.all_user_tweets)
        self.goto_tweet.clicked.connect(self.random_tweet)

    def user_prof_data(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def all_user_tweets(self):
        self.stackedWidget.setCurrentIndex(2)

    def random_tweet(self):
        self.stackedWidget.setCurrentIndex(3)

    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    sys.exit(app.exec_())