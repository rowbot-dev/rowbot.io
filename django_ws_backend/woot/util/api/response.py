
from util.merge import merge

from .constants import constants

class Response():
  def __init__(self, description=None, server_types=None):
    self.description = description
    self.server_types = server_types
    self.value = None
    self.errors = []
    self.children = {}
    self.template = None
    self.empty = False

  def add_error(self, error):
    self.errors.append(error)
    return self

  def add_child(self, child_name, child):
    self.children.update({child_name: child})
    return self

  def add_value(self, value):
    self.value = value
    return self

  def render(self):
    rendered_response = self.render_description_and_types()

    if rendered_response:
      if self.errors:
        rendered_response.update({constants.ERRORS: self.render_errors()})

      if self.value or self.children:
        rendered_response.update({constants.VALUE: self.render_value()})

      return rendered_response

    if self.errors:
      return {constants.ERRORS: self.render_errors()}

    if self.value or self.children:
      return self.render_value()

  def render_description_and_types(self):
    if self.empty:
      rendered = {
        constants.DESCRIPTION: self.description,
        constants.SERVER_TYPES: {
          _type._type: _type.description
          for _type in self.server_types
        },
      }

      if self.template:
        rendered.update({constants.TEMPLATE: self.template.render()})

      return rendered

  def render_errors(self):
    rendered_errors = {}
    for error in self.errors:
      rendered_errors.update({error.code: error.render()})

    return rendered_errors

  def render_value(self):
    if self.children:
      rendered_children = {}
      for child_key, child in self.children.items():
        rendered_children.update({child_key: child.render()})

      return rendered_children

    if isinstance(self.value, list):
      return [
        child.render()
        for child in self.value
      ]

    return self.value
