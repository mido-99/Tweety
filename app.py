from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize
import sys
import json


class TweetyScrapy(QMainWindow):
    
    state = True
    
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
        self.goto_profile.clicked.connect(self.goto_user_prof_data)
        self.goto_user_tweets.clicked.connect(self.goto_all_user_tweets)
        self.goto_tweet.clicked.connect(self.goto_random_tweet)
        self.prof_url_btn.clicked.connect(self.get_profile)
        self.user_twts_btn.clicked.connect(self.get_user_tweets)
        self.tweet_btn.clicked.connect(self.get_tweet)
        

    def goto_user_prof_data(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def goto_all_user_tweets(self):
        self.stackedWidget.setCurrentIndex(2)

    def goto_random_tweet(self):
        self.stackedWidget.setCurrentIndex(3)

    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def get_profile(self):
        '''Get profile data when "Get" button is clicked'''

        self.loading(self.loading_anim)
    
    def get_user_tweets(self):
        '''Get User Tweets when "Get" button is clicked'''

        self.loading(self.loading_anim_2)
    
    def get_tweet(self):
        '''Get User Tweets when "Get" button is clicked'''

        self.loading(self.loading_anim_3)
    
    def loading(self, label_name):
        
        if self.state:
            self.gif_start("icons/loading_white_back.gif", label_name)
        else:
            self.gif_stop(label_name)
        self.state = not self.state

    def gif_start(self, gif_path, label_name):
        '''Plays a Loading gif while working in the background'''

        loading_gif = QMovie(gif_path)
        label_name.setMovie(loading_gif)
        loading_gif.start()
        label_name.setScaledContents(True)
        label_name.setVisible(True)
        label_name.loading_gif = loading_gif

    def gif_stop(self, label_name):
        """Stop gif playing in passed Qlabel"""
        
        if hasattr(label_name, 'loading_gif'):
            label_name.loading_gif.stop()
            label_name.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    sys.exit(app.exec_())