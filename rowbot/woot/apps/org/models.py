# woot.apps.org.models

# django
from django.db import models

# local


# util


### Models

# role specific managers
class ComitteeMemberManager(models.Manager): # search for all the members of a boatclub that are captains
  pass

class RowerManager(models.Manager):
  pass

class CoachManager(models.Manager):
  pass

class CoxManager(models.Manager):
  pass

class SubscriberManager(models.Manager):
  pass

# 1. boat club definitions
class RowingClub(models.Model):
  '''
  What questions do I want to answer about a rowing club?
  1. How many members are there? What types/roles?
  2. What races do they organise/participate in?
  3. What is their record?
  4. What is their relationship with other rowing clubs?

  '''


  # connections


  # properties


  # managers
  committee_members = ComitteeMemberManager()
  rowers = RowerManager()
  coaches = CoachManager()
  coxes = CoxManager()
  subscribers = SubscriberManager()

# 2. boats
class Boat(models.Model):
  '''
  What questions do I want to answer about a boat?
  1. When was it last used?
  2. Who is it booked for next?
  3. Who owns it?
  4. Where is it?
  5. What type? make? weight? age? cost? size? status? spares?

  '''

  #connections
  club = models.ForeignKey(RowingClub, related_name='boats')

  #properties
  # type? make? weight? age? cost? size? status? spares?

# 3. teams
class Team(models.Model):
  '''
  What do I want to know about a team?
  1. Who is in it?
  2. What club is it a part of?
  3. How has it changed from event to event?
  4. What is its record? races? events? training?
  5. 10 outing rule? river usage rules? M1?

  '''

  #connections
  club = models.ForeignKey(RowingClub, related_name='teams')

  #properties
  name = models.CharField(max_length=255)

class

class TeamInstance(models.Model):
  #connections
  club = models.ForeignKey(RowingClub, related_name='team_instances')
  team = models.ForeignKey(Team, related_name='instances')

  #properties
