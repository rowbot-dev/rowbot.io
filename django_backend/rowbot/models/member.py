
# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Local
from rowbot.models.base import Model, random_key

# Util
import uuid
import urllib3
http = urllib3.PoolManager(retries=False)

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

  # Methods
  def activate(self, activation_key):
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
    msg.send()
    return self.activation_email_key

  def new_socket_token(self):
    active_socket_token = self.socket_tokens.get(is_active=True)
    previous = None
    if active_socket_token is not None:
      previous = active_socket_token._id
      active_socket_token.is_active = False
      active_socket_token.save()

    new_socket_token = self.socket_tokens.create()

    try:
      # make request to websocket server
      http.request('GET', 'http://{}:{}/{}.{}'.format(settings.WEBSOCKET['host'], settings.WEBSOCKET['message'], previous, new_socket_token._id))
    except urllib3.exceptions.NewConnectionError:
      print('Connection to websocket server failed.')

    return new_socket_token

class WebSocketAccessToken(Model):
  class Meta:
    permissions = ()

  # Connections
  member = models.ForeignKey('rowbot.Member', related_name='socket_tokens')

  # Properties
  is_active = models.BooleanField(default=True)
