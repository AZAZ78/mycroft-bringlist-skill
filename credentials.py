#!/usr/bin/env python

import base64
import pickle
from BringApi.BringApi import BringApi

try:
    input = raw_input
except NameError:
    pass

email = str(input('Your login/email: '))
password = str(input('Your password: '))

uuid, uuidlist = BringApi.login(email, password)
if uuid is None:
    print('Failed to get credentials')

credentials = {'uuid': uuid, 'list': uuidlist}

with open('/opt/mycroft/skills/mycroft-bringlist-skill.azaz78/credentials.store', 'wb') as f:
    pickle.dump(credentials, f, pickle.HIGHEST_PROTOCOL)
