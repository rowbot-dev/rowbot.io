
# util
from os.path import exists, join
import json

# open settings config
conf_path = './settings/conf.json'
data = None
if exists(conf_path):
  with open(conf_path, 'r+') as settings_json:
    data = json.loads(settings_json.read())
