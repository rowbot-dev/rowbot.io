
# Django
from django.conf.urls import url
from django.http import JsonResponse

# DRF
from rest_framework import routers

# BaseRouter
class SchemaRouter(routers.SimpleRouter):

  def register(self, prefix, viewset, base_name=None):
    if base_name is None:
      base_name = self.get_default_base_name(viewset)
    self.registry.append((prefix, viewset, base_name))

  def schema_view(self, request):
    return JsonResponse(self.schema)

  def get_urls(self):
    """
    Use the registered viewsets to generate a list of URL patterns.
    """
    ret = []

    self.schema = {}
    for prefix, viewset, basename in self.registry:
      lookup = self.get_lookup_regex(viewset)
      routes = self.get_routes(viewset)

      # add to schema
      self.schema[viewset.queryset.model.__name__] = {
        'prefix': prefix,
        'routes': {},
        'basename': basename,
        'fields': list(viewset.serializer.Meta.fields),
      }

      for route in routes:
        # Only actions which actually exist on the viewset will be bound
        mapping = self.get_method_map(viewset, route.mapping)
        if not mapping:
          continue

        # Build the url pattern
        regex = route.url.format(
          prefix=prefix,
          lookup=lookup,
          trailing_slash=self.trailing_slash
        )

        # If there is no prefix, the first part of the url is probably
        #   controlled by project's urls.py and the router is in an app,
        #   so a slash in the beginning will (A) cause Django to give
        #   warnings and (B) generate URLS that will require using '//'.
        if not prefix and regex[:2] == '^/':
          regex = '^' + regex[2:]

        view = viewset.as_view(mapping, **route.initkwargs)
        name = route.name.format(basename=basename)
        ret.append(url(regex, view, name=name))
        self.schema[viewset.queryset.model.__name__]['routes'].update({name: regex})

    ret.append(url(r'schema', self.schema_view, name='schema'))

    return ret
