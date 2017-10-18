
# Django
from django.core.management.base import BaseCommand, CommandError

# DRF
from rest_framework.authtoken.models import Token

# Local
from row.models import Member

# Command
class Command(BaseCommand):
  def handle(self, *args, **options):
    member, member_created = Member.objects.get_or_create(username='npiano', first_name='Nicholas', last_name='Piano', email='nicholas.d.piano@gmail.com')
    member.set_password('mach')
    member.save()
    token, token_created = Token.objects.get_or_create(user=member)
    print(token.key)
