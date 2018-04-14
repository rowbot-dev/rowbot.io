
from django.db import models
from apps.base.models import Model

class Group(Model):

  name = models.CharField(max_length=255)


class User(Model):

  public_key = models.TextField()


class AuthenticationToken(Model):

  user = models.ForeignKey(User, related_name='tokens', on_delete=models.CASCADE)

  payload = models.TextField()
  signature = models.TextField()


class RoleType(Model):

  group = models.ForeignKey(Group, related_name='role_types', on_delete=models.CASCADE)

  name = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class Role(Model):

  type = models.ForeignKey(RoleType, related_name='roles', on_delete=models.CASCADE)
  user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)


class PermissionType(Model):

  role_type = models.ForeignKey(Group, related_name='permission_types', on_delete=models.CASCADE)

  name = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class Permission(Model):

  type = models.ForeignKey(PermissionType, related_name='permissions', on_delete=models.CASCADE)
  role = models.ForeignKey(Role, related_name='permission', on_delete=models.CASCADE)
