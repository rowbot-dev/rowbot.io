#!/usr/bin/env python
import os
import sys
import json

if __name__ == '__main__':
  with open('./env.json') as env_file:
    env_data = json.loads(env_file.read())

  os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_data['settings'])
  try:
    from django.core.management import execute_from_command_line
  except ImportError as exc:
    raise ImportError(
      "Couldn't import Django. Are you sure it's installed and "
      "available on your PYTHONPATH environment variable? Did you "
      "forget to activate a virtual environment?"
    ) from exc
  execute_from_command_line(sys.argv)
