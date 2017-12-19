
# extend common
from settings.common import *

# util
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

##################################################################################################
########################################## NICHOLAS PIANO LOCAL CONFIGURATION
##################################################################################################
### Parameters overridden by Nicholas Piano is his local environment

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION


########## WEBSOCKET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
WEBSOCKET = {
  'host': 'localhost',
  'socket': 4000,
  'message': 3000,
}
########## END WEBSOCKET CONFIGURATION


########## REDIS CONFIGURATION
jobstores = {
  # 'default': MemoryJobStore(),
  'default': RedisJobStore(jobs_key='ap_scheduler.jobs', run_times_key='ap_scheduler.run_times', host='localhost', port=6379)
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
