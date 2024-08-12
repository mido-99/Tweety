from PyQt5.QtCore import  pyqtSignal, QThread
from user_tweets import UserTweets


class ProfileThread(QThread):
    
    profile_data_ready = pyqtSignal(dict)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        user = UserTweets(self.url)
        data = user.get_profile_data()
        self.profile_data_ready.emit(data)

