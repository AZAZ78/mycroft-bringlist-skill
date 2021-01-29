import pickle
import base64

from os import listdir, path  # makedirs, remove,
from os.path import dirname, join  # exists, expanduser, isfile, abspath, isdir

from BringApi.BringApi import BringApi

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

__author__ = 'azaz78'

class BringlistSkill(MycroftSkill):
    def __init__(self):
        super().__init__(name="BringlistSkill")
        self._bring = None

    def initialize(self):
        # handle credentials
        credentials = self._load_credentials_store()
        if credentials:
            self.uuid = credentials['uuid']
            self.uuidlist = credentials['list']
        else:
            self.login = self.settings.get("login", "")
            self.password = self.settings.get("password", "")
            self.uuid, self.uuidlist = BringApi.login(email, password)

        if self.uuid == None:
            self.speak_dialog('bring.error.connect')
            self.log.warning("Loading credentials failed, please check your credentials")
        else:
            self.log.info("Loaded credentials")
            self._bring = BringApi(self.uuid, self.uuidlist)
            if self._bring is None:
                self.speak_dialog('bring.error.connect')
                self.log.warning("API connect failed")
            else:
                self.log.info("API connect succeeded")

    @intent_handler(IntentBuilder('AddItemToBringlist').require('bring.add'))
    def handle_bringlist_add(self, message):
        item = message.data.get('Item')
        self.speak_dialog('bring.error.add', data={"Item": item})

    @intent_handler(IntentBuilder('RemoveItemFromBringlist').require('bring.remove'))
    def handle_bringlist_add(self, message):
        item = message.data.get('Item')
        self.speak_dialog('bring.error.remove', data={"Item": item})

    @intent_handler(IntentBuilder('ClearBringlist').require('bring.clear'))
    def handle_bringlist_add(self, message):
        self.speak_dialog('bring.error.clear')

    def _load_credentials_store(self):
        credentials = {}
        skill_dir = dirname(__file__)
        credentials_file = 'credentials.store'
        if path.exists(skill_dir):
            file_list = listdir(skill_dir)
            if credentials_file in file_list:
                with open(skill_dir + '/' + credentials_file, 'rb') as f:
                    credentials = pickle.load(f)
        return credentials

def create_skill():
    return BringlistSkill()

