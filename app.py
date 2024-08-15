from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog,
    QInputDialog)
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize
import sys
import re
import json
from worker import ProfileThread, TweetsThread


class TweetyScrapy(QMainWindow):
    
    def __init__(self):
        super(TweetyScrapy, self).__init__()
        uic.loadUi('main.ui', self)
        self.handle_buttons()
        self.handle_comboboxes()
        self.setUi()
    
    def setUi(self):
        '''Setup UI elements that need to be set from code'''
        
        self.backButtons()

    def backButtons(self):
        """Setup backButtons of pages & set their common functions"""
        
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
        self.pushButton.clicked.connect(self.test)
        self.goto_profile.clicked.connect(self.goto_user_prof_data)
        self.goto_user_tweets.clicked.connect(self.goto_all_user_tweets)
        self.goto_tweet.clicked.connect(self.goto_random_tweet)
        self.prof_url_btn.clicked.connect(self.get_profile)
        self.user_twts_btn.clicked.connect(self.get_user_tweets)
        self.tweet_btn.clicked.connect(self.get_tweet)
        self.export_prof_btn.clicked.connect(self.export_prof_data)
        self.prof_dir_btn.clicked.connect(self.select_prof_dir)

    def handle_comboboxes(self):
        self.tweets_num_combo.activated.connect(self.handle_custom_number)
    def goto_user_prof_data(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def goto_all_user_tweets(self):
        self.stackedWidget.setCurrentIndex(2)

    def goto_random_tweet(self):
        self.stackedWidget.setCurrentIndex(3)

    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)
    
    #########   Profile Data Page    #########
    

    def get_profile(self):
        '''Get profile data when "Get" button is clicked'''
        
        url = self.prof_url_line.text()
        if self.is_valid_X_user_url(url) and self.tweets_num_spin:
            self.loading(self.loading_anim, start=True)

            # Profile data parsing
            self.prof_worker = TweetsThread(url, )
            self.prof_worker.profile_data_ready.connect(self.on_profile_data_ready)
            self.prof_worker.start()
            # print(url)

        else:
            QMessageBox.warning(self, 'Invalid Input!',
                "Please enter a valid x account url!\n (Only twitter.com & x.com Domains are allowed)"
            )
    
    def is_valid_X_user_url(self, string):
        '''Validate passed text is a valid x.com url'''

        return bool(
            re.match(r'''(https:\/\/(twitter|x).com\/([A-z0-9_]+))$''', string)
        )
    
    def on_profile_data_ready(self, data):
        
        if data != '':
            self.data = data
            self.prof_json_plainEdit.setPlainText(json.dumps(data, indent=2, ensure_ascii=False))
        self.loading(self.loading_anim, start=False)

    def export_prof_data(self):
        '''Export profile data into selected json file'''

        filename = self.export_prof_data_edit.text()

        # if user clicked export with no data
        if self.prof_json_plainEdit.toPlainText() == '':
            QMessageBox.warning(self, 'Error', 'No Data!\n'
                'Please search for a username first to get its data')
            return None
        
        # if user clicked export  with invalid file path
        if filename != '':          # re.match(r'''[^<>:;,?"*|/^]+$''', filename) json validation for future
            if not filename.endswith('.json'):
                filename += '.json'
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.prof_json_plainEdit.toPlainText())
                QMessageBox.information(self, 'Success!', f'Data Exported to {filename}')
            except:
                QMessageBox.critical(self, 'Json Error!', 'Error occured while exporting to json file')
                return None
        else:
            QMessageBox.critical(self, 'Error', 'Export failed!\n'
                'Please check file name, extension, or existing file with the same name')

    def select_prof_dir(self):
        '''Select filename to save profile data to'''

        username = self.data.get('username', '') if hasattr(self, 'data') else ''
        filename = QFileDialog.getSaveFileName(self, 'Save as', username, "JSON files (*.json)")[0]
        self.export_prof_data_edit.setText(filename)
        
    
    #########   User Tweets Page    #########
    
    def test(self):
        
        print(self.valid_tweets_input())
        
    def handle_custom_number(self, index):
        
        numbers_list = [self.tweets_num_combo.itemText(i) for i in range(self.tweets_num_combo.count())]

        if self.tweets_num_combo.itemText(index) == "Custom":
            number, ok = QInputDialog.getInt(self, 'User Tweets', 'Select tweets number to get', 1, 1, 10000)
            if ok:
                if str(number) not in numbers_list:     # If input doesn't exist
                    self.tweets_num_combo.insertItem(self.tweets_num_combo.count() -1, str(number))
                self.tweets_num_combo.setCurrentText(str(number))
        
    def get_user_tweets(self):
        '''Get User Tweets when "Get" button is clicked'''

    def get_tweet(self):
        '''Get User Tweets when "Get" button is clicked'''

        self.loading(self.loading_anim_3)
    
    def loading(self, label_name, start=True):
        """Show loading gif animation while parsing occurs in background"""

        if start:
            self.gif_start("icons/loading_white_back.gif", label_name)
        else:
            self.gif_stop(label_name)

    def gif_start(self, gif_path, label_name):
        '''Play a Loading gif animation'''

        loading_gif = QMovie(gif_path)
        label_name.setMovie(loading_gif)
        loading_gif.start()
        label_name.setScaledContents(True)
        label_name.setVisible(True)
        label_name.loading_gif = loading_gif

    def gif_stop(self, label_name):
        """Stop loading gif animation"""
        
        if hasattr(label_name, 'loading_gif'):
            label_name.loading_gif.stop()
            label_name.setVisible(False)
            del label_name.loading_gif


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    sys.exit(app.exec_())