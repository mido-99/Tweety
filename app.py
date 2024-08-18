from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox,
    QFileDialog, QInputDialog, QWidget)
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize

import sys
import os
import re
import json
import dotenv 
from functools import partial

from worker import ProfileThread, TweetsThread
from custom_widgets import GifButton
from styling import STYLESHEET


class TweetyScrapy(QMainWindow):
    
    COOKIE = None
    
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setUi()
        self.handle_buttons()
        self.handle_comboboxes()
    
    def setUi(self):
        '''Setup UI elements that need to be set from code'''
        
        self.setWindowTitle('X Scraper')
        self.setWindowIcon(QIcon('icons/x_logo.jpg'))   #<a href="https://www.freepik.com/free-vector/new-2023-twitter-x-logo-black-background_57643008.htm#query=x%20logo&position=17&from_view=keyword&track=ais_hybrid&uuid=a5b000e0-0af2-476e-b384-21f1da14cd59">Image by starline</a> on Freepik
        self.backButtons()
        self.helpButtons()
        
        self.setStyleSheet(STYLESHEET)

    def backButtons(self):
        """Setup backButtons of pages & set their common functions"""
        
        back_pix = QIcon('icons/back.jpg')
        back_btns = [btn for btn in self.findChildren(QPushButton) if 'backButton' in btn.objectName()]

        for btn in back_btns:
            # UI
            btn.setIcon(back_pix)
            btn.setIconSize(QSize(30, 30))
            btn.setGeometry(0, 0, 30, 30)
            # Function
            btn.clicked.connect(self.go_home)
    
    def helpButtons(self):
        """Setup custom help buttons to show help about how to add cookie"""

        for idx in range(self.stackedWidget.count()):
            # UI
            page = self.stackedWidget.widget(idx)            
            button = GifButton('icons/help_slow.gif', 'cookie', page)
            button.setGeometry(700, 0, 100, 40)
            
            # print(f"pos(): {button.pos()}")
            # print(f"x(): {button.x()}")
            # print(f"y(): {button.y()}")
            # print(f"rect(): {button.rect()}")
            # print(f"size(): {button.size()}")

            # Function
            button.clicked.connect(self.show_help)
    
    def handle_buttons(self):
        
        self.pushButton.clicked.connect(self.test)
        # Home page
        self.goto_profile.clicked.connect(self.goto_user_prof_data)
        # self.goto_profile.setDefault(True)
        self.goto_user_tweets.clicked.connect(self.goto_all_user_tweets)
        # Profile page
        self.prof_url_btn.clicked.connect(self.get_profile)
        self.export_prof_btn.clicked.connect(partial(self.export_json_data, 
            self.export_prof_data_line, self.prof_json_plainEdit))
        self.prof_dir_btn.clicked.connect(self.select_prof_dir)
        # User tweets page
        self.user_twts_btn.clicked.connect(self.get_user_tweets)
        self.export_tweets_btn.clicked.connect(partial(self.export_json_data, 
            self.export_tweets_line, self.tweets_json_plainEdit))
        self.tweets_dir_btn.clicked.connect(self.select_tweets_dir)

    def handle_comboboxes(self):
        self.tweets_num_combo.activated.connect(self.handle_custom_number)

    # Navigation Buttons
    def goto_user_prof_data(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def goto_all_user_tweets(self):
        self.stackedWidget.setCurrentIndex(2)

    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def test(self):
        pass

    # Check existing cookies
    def cookie_exists(self):
        
        return bool(self.COOKIE)

    def check_cookie(self):
        '''Checks if there's existing twitter session cookies in "cookies" file'''

        if os.path.exists('cookie.env'):
            self.COOKIE = dotenv.dotenv_values('cookie.env')['cookie']
        else:
            QMessageBox.information(self, 'Cooke not found!',
                '''Make sure to add "cookie.env" file in app's directory 
                with logged in cookies.''')


    #*###########   Profile Data Page    #############
    
    def get_profile(self):
        '''Get profile data when "Get" button is clicked'''
        
        while not self.cookie_exists():
            QMessageBox.critical(self, 'Cookie Needed!', '''
                    Please create "cookie.env" file in app's directory first!
                '''.strip()
                )
            return False
        
        url = self.prof_url_line.text()
        if self.is_valid_X_user_url(url):
            self.loading(self.loading_anim, start=True)
            self.prof_user = url.split('/')[-1]

            # Profile data parsing
            self.prof_worker = ProfileThread(url)
            self.prof_worker.profile_data_ready.connect(self.on_profile_data_ready)
            self.prof_worker.start()
            # print(url)

        else:
            QMessageBox.warning(self, 'Invalid URL!',
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
        
    def select_prof_dir(self):
        '''Select filename to save profile data to'''

        username = self.prof_user if hasattr(self, 'prof_user') else ''
        filename = QFileDialog.getSaveFileName(self, 'Save as', username, "JSON files (*.json)")[0]
        self.export_prof_data_line.setText(filename)


    #*#########   User Tweets Page    ###########

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

        while not self.cookie_exists():
            QMessageBox.critical(self, 'Cookie Needed!', '''
                    Please create "cookie.env" file in app's directory first!
                '''.strip()
                )
            return False

        url = self.user_twts_edit.text()
        number = self.tweets_num_combo.itemText(self.tweets_num_combo.currentIndex())

        if self.is_valid_X_user_url(url):
            self.loading(self.loading_anim_2, start=True)
            self.tweets_user = url.split('/')[-1]

            # Tweets data parsing
            self.tweets_worker = TweetsThread(url, int(number))
            self.tweets_worker.tweets_ready.connect(self.on_tweets_ready)
            self.tweets_worker.start()
            # print(url)

        else:
            QMessageBox.warning(self, 'Invalid Input!',
                "Please enter a valid x account url!\n (Only twitter.com & x.com Domains are allowed)"
            )
    
    def select_tweets_dir(self):
        '''Select filename to save profile data to'''

        username = self.tweets_user if hasattr(self, 'tweets_user') else ''
        filename = QFileDialog.getSaveFileName(self, 'Save as', f"{username}_tweets", "JSON files (*.json)")[0]
        self.export_tweets_line.setText(filename)
    
    def on_tweets_ready(self, data):
        
        if data != '':
            self.data = data
            self.tweets_json_plainEdit.setPlainText(json.dumps(data, indent=2, ensure_ascii=False))
        self.loading(self.loading_anim_2, start=False)


    #*#############     General methods     ##############
    
    def show_help(self):
        #TODO To be named "cookie_help", while current message to be moved to "desclaimer" 
        #TODO May need to move them to custom_widgets then add ! button in UI
        
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet(STYLESHEET)
        msg_box.setStyleSheet('''QLabel{min-width: 700px;}''')

        msg_box.setWindowTitle("Important Notice Regarding Scraping on X (Twitter)")
        msg_box.setText('''
            Before proceeding with scraping data from X, it's crucial to understand the potential risks and responsibilities involved.\n
            Recent updates to X's platform have introduced stricter measures to protect user data and privacy. As a result, certain actions, including scraping, may require you to include your logged-in session cookies to access specific information.

            What This Means?
            Cookies and Account Identification: When you use your session cookies to scrape data from X, the platform can directly associate the activity with your personal account. This means that X can identify your account as the source of the scraping activity.

            Potential Consequences: Engaging in scraping activities, especially with your logged-in session cookies, may violate X's terms of service. X may detect this behavior and take actions against your account. Consequences can range from temporary limitations on your account to a complete suspension.

            Your Responsibility:
            Be Cautious! If you decide to proceed with scraping X, you do so at your own risk. \n
            While staying at normal scraping rate can go unnoticed, Be aware that you are fully responsible for any actions taken by X as a result of your activities. 
        '''.replace('  ', ''))

        # # Set the size of the QMessageBox

        msg_box.exec_()
    
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
    
    def export_json_data(self, export_filepath_lineEdit, json_data_plainTextEdit):
        '''Export profile data into selected json file'''

        filename = export_filepath_lineEdit.text()

        # if user clicked export with no data
        if json_data_plainTextEdit.toPlainText() == '':
            QMessageBox.warning(self, 'Error', 'No Data!\n'
                'Please search for a username first to get its data')
            return None
        
        # if user clicked export  with invalid file path
        if filename != '':          # re.match(r'''[^<>:;,?"*|/^]+$''', filename) json validation for future
            if not filename.endswith('.json'):
                filename += '.json'
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(json_data_plainTextEdit.toPlainText())
                QMessageBox.information(self, 'Success!', f'Data Exported to\n {os.path.basename(filename)}')
            except:
                QMessageBox.critical(self, 'Json Error!', 'Error occured while exporting to json file')
                return None
        else:
            QMessageBox.critical(self, 'Error', 'Export failed!\n'
                'Please check file name, extension, or existing file with the same name')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TweetyScrapy()
    window.show()
    window.check_cookie()
    sys.exit(app.exec_())