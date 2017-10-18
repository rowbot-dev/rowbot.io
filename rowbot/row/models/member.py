
# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# DRF


# Local
from row.models.base import Model, random_key

# Util
import uuid

# Member
class MemberManager(BaseUserManager):
  pass

# m = Member.objects.create(username='npiano', email='nicholas.d.piano@gmail.com', first_name='Nicholas', last_name='Piano')
class Member(AbstractBaseUser, PermissionsMixin, Model):
  USERNAME_FIELD = 'username'

  ### Manager
  objects = MemberManager()

  ### Connections


  ### Properties
  # identification
  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(max_length=255)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  # activation
  is_activated = models.BooleanField(default=False)
  activation_email_sent = models.BooleanField(default=False)
  activation_key = models.UUIDField(default=uuid.uuid4)
  activation_email_key = models.CharField(max_length=8, default=random_key)

  # administration
  is_enabled = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
