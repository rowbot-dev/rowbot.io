
from django.core.management.base import BaseCommand, CommandError

from apps.rowbot.models import Member

# Command
class Command(BaseCommand):
  def handle(self, *args, **options):
    member, member_created = Member.objects.get_or_create(username='npiano', first_name='Nicholas', last_name='Piano', email='nicholas.d.piano@gmail.com')
    member.set_password('mach')
    member.is_activated = True
    member.save()
