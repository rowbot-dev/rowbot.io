
### Django
from django.db import models

### Local
from apps.rowbot.models.base import Model

### Event
class Event(Model):
	_label = 'event'

	### Connections
	group = models.ForeignKey('rowbot.Group', related_name='events')

	### Properties
	name = models.CharField(max_length=255)
	description = models.TextField()

class EventInstance(Model):
	_label = 'eventinstance'

	### Connections
	event = models.ForeignKey('rowbot.Event', related_name='instances')

	### Properties
	description = models.TextField()

class EventToken(Model):
	_label = 'eventtoken'

	### Connections
	group = models.ForeignKey('rowbot.Group', related_name='tokens')
	event = models.ForeignKey('rowbot.EventInstance', related_name='tokens')