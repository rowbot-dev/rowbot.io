
# Django
from django.core.management.base import BaseCommand, CommandError

# Local
from apps.rowbot.models import Club, Member, RoleModel, Role

# Command
class Command(BaseCommand):
  def handle(self, *args, **options):
    for i in range(2):
      club, club_created = Club.objects.get_or_create(name='TestClub{}'.format(i))
      member = Member.objects.get(username='npiano')

      # roles
      model, model_created = RoleModel.objects.get_or_create(club=club, reference='admin', verbose_name='Admin', verbose_name_plural='Admins', description='Administrator of the club. Is able to access and manipulate all aspects of the clubs data.')
      role, role_created = Role.objects.get_or_create(model=model, member=member)
