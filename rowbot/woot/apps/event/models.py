# woot.apps.event.models

# django
from django.db import models

# local


# util


### Models
class Event(models.Model):
  '''
  The type of an object with a subclass can be determined by testing with: hasattr(class, 'subclass_var_name') -> bool
  e.g. hasattr(event, 'outing')

  The Event class defines a general model for a recurring event. Events are by nature recurring, but the EventInstance
  class describes a single, non-recurring element of its existance. I have CellInstance to thank for this. This principle
  can also be applied to a person fulfilling a role; a "MemberInstance".

  '''

  # connections

  # properties

class Outing(Event):
  # connections

  # properties
  pass

class Race(Event):
  # connections

  # properties
  pass

class TrainingSession(Event):
  # connections

  # properties
  pass

class EventInstance(models.Model):
  # connections

  # properties
  pass
