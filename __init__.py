from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

from os import listdir, path  # makedirs, remove,
from os.path import dirname, join  # exists, expanduser, isfile, abspath, isdir

from BringApi.BringApi import BringApi

import pickle
import base64
import re

__author__ = 'azaz78'

class BringlistSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__(name="BringlistSkill")
        self._bring = None

    def initialize(self):
        # handle credentials
        credentials = self._load_credentials_store()
        if credentials:
            uuid = credentials['uuid']
            uuidlist = credentials['list']
        else:
            login = self.settings.get("login", "")
            password = self.settings.get("password", "")
            uuid, uuidlist = BringApi.login(login, password)

        if uuid == None:
            self.speak_dialog('bring.error.connect')
            self.log.warning("Loading credentials failed, please check your credentials")
        else:
            self.log.info("Loaded credentials")
            self._bring = BringApi(uuid, uuidlist)
            if self._bring is None:
                self.speak_dialog('bring.error.connect')
                self.log.warning("API connect failed")
            else:
                self.log.info("API connect succeeded")

    @intent_handler(IntentBuilder("AddToBringlist")
                                      .require("bring.list")
                                      .require("bring.add"))
    def handle_bringlist_add(self, message):
        self.log.info("Bringlist add")

        item, desc = self._get_item(message.data.get('utterance'), 'bring.add.regex')
        if item:
            self._bring.purchase_item(item.capitalize(), desc)
            self.speak_dialog('bring.success.add', data={"Item": item})
        else:
            self.speak_dialog('bring.error.add', data={"Item": item})

    @intent_handler(IntentBuilder("RemoveFromBringlist")
                                      .require("bring.list")
                                      .require("bring.remove"))
    def handle_bringlist_remove(self, message):
        self.log.info("Bringlist remove")

        item, desc = self._get_item(message.data.get('utterance'), 'bring.remove.regex')
        if item:
            self._bring.remove_item(item.capitalize())
            self.speak_dialog('bring.success.remove', data={"Item": item})
        else:
            self.speak_dialog('bring.error.remove', data={"Item": item})

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

    def _get_item(self, text, regfile):
        with open(self.find_resource(regfile,'regex')) as f:
           matcher = f.readline().rstrip('\n')
           match = re.match(matcher, text)
           if match:
              return match.group('Item'), match.group('Desc') if match.group('Desc') is not None else "" 
           else:
              return None, None

def create_skill():
    return BringlistSkill()

