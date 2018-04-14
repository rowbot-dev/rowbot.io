
# DRF
from rest_framework.permissions import BasePermission

# Permissions
class IsSelf(BasePermission):
  def has_permission(self, request, view):
    return True

  def has_object_permission(self, request, view, obj):
    print(request, view, obj)
    '''
    Return true if the request.user matches the obj
    '''
    return request.user == obj
