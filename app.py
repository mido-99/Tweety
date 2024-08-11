from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize
import sys
import json


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
        self.goto_profile.clicked.connect(self.goto_user_prof_data)
        self.goto_user_tweets.clicked.connect(self.goto_all_user_tweets)
        self.goto_tweet.clicked.connect(self.goto_random_tweet)
        self.prof_url_btn.clicked.connect(self.get_profile)
        

    def goto_user_prof_data(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def goto_all_user_tweets(self):
        self.stackedWidget.setCurrentIndex(2)

    def goto_random_tweet(self):
        self.stackedWidget.setCurrentIndex(3)

    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def get_profile(self):
        '''Gets profile data when "Get" button is clicked'''

        profile_data = json.dumps({self.prof_url_edit.text(): 'first', 2: 'second'})
        self.prof_json_plainEdit.setPlainText(profile_data)
        self.animate_loading("icons/loading_white_back.gif", self.loading_anim)
        

    def animate_loading(self, gif_path, label_name):
        '''Plays a Loading gif while working in the background'''

        loading_gif = QMovie(gif_path)
        label_name.setMovie(loading_gif)
        loading_gif.start()
        label_name.setScaledContents(True)
        label_name.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    sys.exit(app.exec_())