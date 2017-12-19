
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


class EventNotificationModel(Model):
  class Meta:
    permissions = ()

  # Connections
  model = models.ForeignKey('rowbot.EventModel', related_name='notification_models')

  # Properties
  name = models.CharField(max_length=255)
  relative_duration = models.DurationField()
  is_negative = models.BooleanField(default=False)
  is_absolute = models.BooleanField(default=False)
  absolute_hour = models.IntegerField(default=0)
  absolute_minute = models.IntegerField(default=0)

  # Methods
  def apply(self, date):
    # return the new date based on the relative_duration and absolute_hour
    # shift by relative component
    if self.is_negative:
      shifted_date = date - self.relative_duration
    else:
      shifted_date = date + self.relative_duration

    # replace time components with those of the absolute_hour and absolute_minute
    if self.is_absolute:
      shifted_date.hour = max(min(self.absolute_hour, 23), 0)
      shifted_date.minute = max(min(self.absolute_minute, 59), 0)

    return shifted_date

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
    # create a set of several notifications based on notification models of the event model
    for notification_model in self.event.model.notification_models.all():
      notification, notification_created = self.notifications.get_or_create(name=notification_model.name)
      if notification_created:
        notification.timestamp = notification_model.apply(self.start_time)
        notification.schedule()
        notification.save()

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
      self.is_active = False
      self.save()
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
