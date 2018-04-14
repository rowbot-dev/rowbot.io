
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from os.path import join, dirname, abspath, exists, normpath
from woot.settings.common import *

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(WOOT_PATH, 'db', 'db.sqlite3')
  }
}

DEBUG = True

########## REDIS CONFIGURATION
jobstores = {
  'default': MemoryJobStore(),
  # 'default': RedisJobStore(jobs_key='ap_scheduler.jobs', run_times_key='ap_scheduler.run_times', host='localhost', port=6379)
}
executors = {
  'default': ThreadPoolExecutor(20),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 3
}
SCHEDULER = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
SCHEDULER.start()
########## END REDIS CONFIGURATION
