
# Django
from django.db import models
from django.conf import settings
from django.utils import timezone

# DRF


# Local
from rowbot.models.base import Model

# Util
from datetime import timedelta
import json
import urllib3
http = urllib3.PoolManager(retries=False)
import uuid
_scheduler = settings.SCHEDULER

# Heirarchy:
# EventModel is a wrapper for an event type, such as a race, an outing, or a training session.
# Example: May Bumps
# Example: Training session

# Event is a wrapper for a specific implementation of that event model.
# Example: May Bumps 2017
# Example: Men's training session on Saturdays

# EventInstance is what actually happens in reality. It is the thing that ultimately reminders are set for.
# Example: May Bumps 2017 > Day 1 > 12:45 - 13:15
# Example: Men's training session, Saturday 12th of June, 2017, 19:45 - 20:45

# Event
class EventModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('rowbot.Club', related_name='event_models')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)


class Event(Model):
  class Meta:
    permissions = ()

  # Connections
  model = models.ForeignKey('rowbot.EventModel', related_name='events')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  name = models.CharField(max_length=255)
  description = models.TextField()
  is_active = models.BooleanField(default=True)

  # Methods
  def clear(self):
    # unschedule all future instances
    pass

  def repeat(self, interval=None):
    # make new event instances at regular intervals
    # reschedule future events in order to new interval
    # if interval is None, refresh number of future event instances scheduled
    pass


class EventInstance(Model):
  class Meta:
    permissions = ()

  # Connections
  event = models.ForeignKey('rowbot.Event', related_name='instances')

  # Properties
  start_time = models.DateTimeField(auto_now_add=False, null=True)
  end_time = models.DateTimeField(auto_now_add=False, null=True)
  location = models.CharField(max_length=255)
  description = models.TextField()
  is_active = models.BooleanField(default=True)

  # Methods
  def cancel(self):
    # unschedule all notifications
    pass

  def schedule(self):
    # create a set of several notifications
    # 1. First one
    first = self.notifications.create(name='first', timestamp=self.end_time - timedelta(seconds=6))
    first.schedule()

    second = self.notifications.create(name='second', timestamp=self.end_time - timedelta(seconds=3))
    second.schedule()

    third = self.notifications.create(name='third', timestamp=self.end_time)
    third.schedule()

def trigger(_id):
  # get the model from the parent and call the trigger function
  EventInstance._meta.get_field('notifications').related_model.objects.get(id=_id).trigger()

class EventNotification(Model):
  class Meta:
    permissions = ()

  # Connections
  event = models.ForeignKey('rowbot.EventInstance', related_name='notifications')

  # Properties
  name = models.CharField(max_length=255)
  timestamp = models.DateTimeField(auto_now_add=False, null=True)
  schedule_id = models.UUIDField(default=uuid.uuid4)
  is_active = models.BooleanField(default=True)

  # Methods
  def trigger(self):
    # all subscribers to the event need to be notified.
    # to do this, retrieve the set of websocket id's and make a request to the node.js server.

    try:
      # make request to websocket server
      http.request('POST', 'http://{}:{}'.format(settings.WEBSOCKET['host'], settings.WEBSOCKET['message']), body=json.dumps({'data': {'ref': self._ref}, 'keys': self.keys()}))
    except urllib3.exceptions.NewConnectionError:
      print('Connection to websocket server failed.')

  def schedule(self):
    _scheduler.add_job(
      trigger,
      args=[self._id],
      trigger='date',
      id=self.schedule_id.hex,
      replace_existing=True,
      run_date=self.timestamp
    )

  def unschedule(self):
    _scheduler.remove_job(self.schedule_id.hex)

  def keys(self):
    return [role_instance.role.member.socket_tokens.get(is_active=True)._id for role_instance in self.event.roles.all()]
