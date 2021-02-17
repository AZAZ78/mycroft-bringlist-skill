#!/usr/bin/env python

import base64
import pickle
from os.path import join
from BringApi.BringApi import BringApi
from mycroft.filesystem import FileSystemAccess

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

file_system = FileSystemAccess(join('skills', 'BringlistSkill'))

with file_system.open('credentials.store', 'wb') as f:
    pickle.dump(credentials, f, pickle.HIGHEST_PROTOCOL)

print('Created credentials.store in {}'.format(file_system.path))
