from mycroft import MycroftSkill, intent_file_handler


class Bringlist(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('bringlist.intent')
    def handle_bringlist(self, message):
        self.speak_dialog('bringlist')


def create_skill():
    return Bringlist()

