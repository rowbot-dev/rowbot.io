
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db import models

from util.merge import merge
from util.api import Schema, types, map_type, errors, constants
from apps.base.models import Model, Manager, random_key
from apps.base.schema import model_schema_constants

import uuid

class MemberManager(BaseUserManager, Manager):
  def schema(self, authorization=None):
    schema = super().schema(authorization=authorization)

    # make modifications based on authorization

    return schema

  def schema_instance_methods(self, authorization=None):
    return Schema(
      description='Methods for the {} model',
      children={
        self.model.send_activation_email.__name__: Schema(
          description='Send the activation email to the member',
          server_types=types.BOOLEAN('A value of true will trigger this method'),
        ),
        self.model.activate.__name__: Schema(
          description='Send the activation email to the member',
          children={
            model_schema_constants.ARGUMENTS: Schema(
              description='',
              children={
                'activation_key': Schema(
                  description='',
                  server_types=types.UUID(),
                ),
              },
            ),
          },
        ),
      },
    )

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
  first_name = models.CharField(max_length=255, default='')
  last_name = models.CharField(max_length=255, default='')

  # activation
  is_activated = models.BooleanField(default=False)
  activation_email_sent = models.BooleanField(default=False)
  activation_key = models.UUIDField(default=uuid.uuid4)
  activation_email_key = models.CharField(max_length=8, default=random_key)

  # administration
  is_enabled = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  # Methods
  def activate(self, activation_key=None):
    if not self.is_activated:
      self.is_activated = activation_key == self.activation_key.hex if activation_key is not None else self.is_activated
      self.save()
    return self.is_activated

  def send_activation_email(self):
    self.activation_key = uuid.uuid4()
    self.activation_email_key = random_key()
    self.activation_email_sent = True
    self.save()

    html_content = render_to_string('rowbot/activation_email.html', {'key': self.activation_key.hex})
    text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives('activation {}'.format(self.activation_email_key), text_content, 'signup@rowbot.com', [self.email])
    msg.attach_alternative(html_content, 'text/html')

    # REAL WORLD NEEDS AN EMAIL ACCOUNT
    # number_of_messages_sent = msg.send()
    # return number_of_messages_sent > 0 # success?

    return True


class AuthenticationToken(Model):

  # Connections
  member = models.ForeignKey('rowbot.Member', related_name='tokens', on_delete=models.CASCADE)

  # Properties
