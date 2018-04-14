
# Django
from django.core.management.base import BaseCommand, CommandError

# Local
from apps.rowbot.models import Club, Member

# Util
import time
from django.utils import timezone
from datetime import timedelta

# Command
class Command(BaseCommand):
  def handle(self, *args, **options):
    club = Club.objects.get(name='TestClub1')
    role = Member.objects.get(username='npiano').roles.get(model__club=club)

    # event model
    event_model, event_model_created = club.event_models.get_or_create(reference='test', verbose_name='Test', verbose_name_plural='Tests')

    # notification models
    first, first_created = event_model.notification_models.get_or_create(name='first', relative_duration=timedelta(seconds=10), is_negative=True)

    # event
    event, event_created = event_model.events.get_or_create(name='Test 1', description='a test')

    # create event instance
    start_time = timezone.now() + timedelta(seconds=20)
    end_time = start_time + timedelta(seconds=20)
    event_instance = event.instances.create(
      start_time=start_time,
      end_time=end_time,
      location='some location',
      description='a test',
    )

    # add role instance
    role_instance = role.instances.create(event=event_instance)

    # schedule
    event_instance.schedule()

    # wait
    time.sleep(30)
