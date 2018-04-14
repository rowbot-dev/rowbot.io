
from os.path import join, dirname, abspath, exists, normpath
from woot.settings.common import *

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(WOOT_PATH, 'db', 'db.sqlite3')
  }
}
