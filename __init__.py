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
        self._bring = None
        self._regex = {}

    def initialize(self):
        # handle credentials
        credentials = self._load_credentials_store()
        if credentials is not None:
            uuid = credentials['uuid']
            uuidlist = credentials['list']
        else:
            login = self.settings.get("login", "")
            password = self.settings.get("password", "")
            uuid, uuidlist = BringApi.login(login, password)

        if uuid is None:
            self.speak_dialog('bring.error.connect')
            self.log.warning("Loading credentials failed, please check your credentials")
        else:
            self.log.info("Loaded credentials")
            self._bring = BringApi(uuid, uuidlist)
            if self._bring is not None:
                self.log.info("API connect succeeded")
                return
                
        self.speak_dialog('bring.error.connect')
        self.log.warning("API connect failed")

    @intent_handler(IntentBuilder("AddToBringlist")
                                      .require("bring.list")
                                      .require("bring.add"))
    def handle_bringlist_add(self, message):
        self.log.info("Bringlist add")
        if self._bring is None:
            self.speak_dialog('bring.error.connect')

        item, desc = self._get_item(message.data.get('utterance'), 'bring.add.regex')
        if item is not None:
            self._bring.purchase_item(item.capitalize(), desc)
            self.speak_dialog('bring.success.add', data={"Item": item})
            return
        self.speak_dialog('bring.error.add', data={"Item": item})

    @intent_handler(IntentBuilder("RemoveFromBringlist")
                                      .require("bring.list")
                                      .require("bring.remove"))
    def handle_bringlist_remove(self, message):
        self.log.info("Bringlist remove")
        if self._bring is None:
            self.speak_dialog('bring.error.connect')

        item, desc = self._get_item(message.data.get('utterance'), 'bring.remove.regex')
        if item:
            self._bring.recent_item(item.capitalize())
            self.speak_dialog('bring.success.remove', data={"Item": item})
            return
        self.speak_dialog('bring.error.remove', data={"Item": item})

    @intent_handler(IntentBuilder("ClearBringlist")
                                      .require("bring.list")
                                      .require("bring.clear"))
    def handle_bringlist_clear(self, message):
        self.log.info("Bringlist clear")
        if self._bring is None:
            self.speak_dialog('bring.error.connect')

        items = self._bring.get_items()['purchase']
        if items:
            for item in items:
                self._bring.recent_item(item['name'])
            self.speak_dialog('bring.success.clear', data={"Count": len(items)})
            return
        self.speak_dialog('bring.error.clear')

    def _load_credentials_store(self):
        credentials = None 
        credentials_file = 'credentials.store'
        if self.file_system.exists(credentials_file):
            with self.file_system.open(credentials_file, 'rb') as f:
                credentials = pickle.load(f)
        return credentials

    def _get_item(self, text, regfile):
        match = self._get_regex(regfile).match(text)
        if match:
            return match.group('Item'), match.group('Desc') if match.group('Desc') is not None else ""
        else:
            return None, None

    def _get_regex(self, regfile):
        if regfile in self._regex:
            return self._regex[regfile]
        with open(self.find_resource(regfile,'regex')) as f:
            matcher = f.readline().rstrip('\n')
            regex = re.compile(matcher)
            self._regex[regfile] = regex
            return regex

def create_skill():
    return BringlistSkill()

