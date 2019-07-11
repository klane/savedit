from dropbox import Dropbox

from savedit.config import DROPBOX_TOKEN
from savedit.services import Service


class DropboxService(Service):
    def __init__(self):
        self.dropbox = Dropbox(DROPBOX_TOKEN)

    @staticmethod
    def check_post(post):
        pass

    @staticmethod
    def is_registered():
        pass

    def is_saved(self, post):
        pass

    def save_post(self, post):
        pass
