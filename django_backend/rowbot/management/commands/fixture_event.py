
# Django
from django.core.management.base import BaseCommand, CommandError

# Local
from rowbot.models import Club, Member

# Util
import time
from django.utils import timezone
from datetime import timedelta

# Command
class Command(BaseCommand):
  def handle(self, *args, **options):
    club = Club.objects.get(name='TestClub1')
    role = Member.objects.get(username='npiano').roles.get(model__club=club)

    # event
    event_model, event_model_created = club.event_models.get_or_create(reference='test', verbose_name='Test', verbose_name_plural='Tests')

    event, event_created = event_model.events.get_or_create(name='Test 1', description='a test')

    start_time = timezone.now()
    end_time = start_time + timedelta(seconds=20)
    event_instance = event.instances.create(
      start_time=start_time,
      end_time=end_time,
      location='some location',
      description='a test',
    )

    role_instance = role.instances.create(event=event_instance)

    event_instance.schedule()

    time.sleep(30)
