# woot.apps.member.models

# django
from django.db import models
from django.contrib.auth.models import (
                                         BaseUserManager,
                                         AbstractBaseUser,
                                         PermissionsMixin
                                       )

# local
from apps.org.models import RowingClub, Team, TeamInstance

# vars

# classes
class MemberManager(BaseUserManager):
  def create_user(self, username, email, password=None):
    """
    Creates and saves a User with the given email, date of
    birth and password.
    """
    if not email:
      raise ValueError('Users must have an email address')

    user = self.model(
      username=username,
      email=self.normalize_email(email),
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, email, password):
    """
    Creates and saves a superuser with the given email, date of
    birth and password.
    """
    user = self.create_user(username, email,
      password=password,
    )
    user.is_admin = True
    user.save(using=self._db)
    return user

class Member(AbstractBaseUser, PermissionsMixin):
  '''
  What will I want to know about a member?
  1. Does he/she row/cox/coach? How much? How many times in the past?
  2. What types of activities/excercises have they done? and when?
  3. What clubs are they a part of and what teams in those clubs?
  4. What is the overall experience or rating of this rower?
  5. What are their current vitals? Heart rate? Weight? Erg times?

  '''

  # properties
  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(verbose_name='email address',max_length=255)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  objects = MemberManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  # member properties
  clubs = models.ManyToManyField(RowingClub, related_name='members') # Fitzwilliam and Eddies
  teams = models.ManyToManyField(Team, related_name='members') # row M1 and cox M2

  # methods
  def get_full_name(self):
    # The user is identified by their email address
    return self.username

  def get_short_name(self):
    # The user is identified by their email address
    return self.username

  def __str__(self):
    return '{}: {}'.format(self.username, self.email)

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True

  @property
  def is_staff(self):
    "Is the user a member of staff?"
    # Simplest possible answer: All admins are staff
    return self.is_admin

### Instance
class Role(models.Model): # a token held by a member to describe their current status is the club
  # connections
  club = models.ForeignKey(RowingClub, related_name='roles')
  member = models.ForeignKey(Member, related_name='roles')

  # properties
  name = models.CharField(max_length=255)

class MemberRoleInstance(models.Model): # an object added to a member at each event to hold details specific to that member/event
  '''
  A member will not be the same from outing to outing or race to race. What things do I want to know about this member after those events?
  1. Did they win?
  2. What was their time?
  3. What excercises did they do?
  4. What position or role did they fill?
  5. Were they late/recieve any penalty?
  6. What comments were left about this event?
  7. Which club and team did they participate for?
  8. What is the overall experience or rating of this rower on a running basis?
  5. What are their current vitals before this event? Heart rate? Weight? Erg times after?

  '''

  #connections
  club = models.ForeignKey(RowingClub, related_name='member_role_instances') # what club is the member rowing for in this event?
  team = models.ForeignKey(TeamInstance, related_name='member_role_instances') # what team is this member currently a part of?
  # event = models.ForeignKey(Event, related_name='participants') # what event is the reason for creating this instance?
  member = models.ForeignKey(Member, related_name='instances') # member this is attached to
  role = models.ForeignKey(Role, related_name='instances') # what role were they filling at this time?

  # properties
  race_count = models.IntegerField(default=0)
  outing_count = models.IntegerField(default=0)
  experience = models.IntegerField(default=0)
  weight = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
