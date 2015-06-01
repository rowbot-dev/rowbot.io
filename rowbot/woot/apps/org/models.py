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
  # connections


  # properties


  # managers
  committee_members = ComitteeMemberManager()
  rowers = RowerManager()
  coaches = CoachManager()
  coxes = CoxManager()
  subscribers = SubscriberManager()

# 2. teams
class Team(models.Model):
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

# 3. boats
class Boat(models.Model):
  #connections
  club = models.ForeignKey(RowingClub, related_name='boats')
  team_instance = models.ForeignKey(TeamInstance, related_name='boats')

  #properties
