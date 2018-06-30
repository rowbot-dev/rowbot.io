
from util.merge import merge

from .modes import modes
from .constants import constants

class Response():
  def __init__(self, description=None, server_types=None, mode=modes.NORMAL):
    self.description = description
    self.server_types = server_types
    self.mode = mode
    self.value = None
    self.errors = []
    self.children = {}
    self.template = None

  def add_error(self, error):
    self.errors.append(error)

  def add_child(self, child_name, child):
    self.children.update({child_name: child})

  def add_value(self, value):
    self.value = value

  def render(self, mode=modes.NORMAL):
    rendered_response = self.render_description_and_types(mode)

    if mode.value >= self.mode.value:
      if rendered_response:
        if self.errors:
          rendered_response.update({constants.ERRORS: self.render_errors()})

        if self.value or self.children:
          rendered_response.update({constants.VALUE: self.render_value(mode)})

        return rendered_response

      if self.errors:
        return {constants.ERRORS: self.render_errors()}

      if self.value or self.children:
        return self.render_value(mode)

  def render_description_and_types(self, mode):
    if mode.value >= modes.VERBOSE.value:
      rendered = {}
      if self.description:
        rendered.update({constants.DESCRIPTION: self.description})

      if self.server_types:
        rendered.update({constants.SERVER_TYPES: {_type._type: _type.description for _type in self.server_types}})

      if self.template:
        rendered.update({constants.TEMPLATE: self.template.render(mode=mode)})

      return rendered

  def render_errors(self):
    rendered_errors = {}
    for error in self.errors:
      rendered_errors.update({error.code: error.render()})

    return rendered_errors

  def render_value(self, mode):
    if self.children:
      rendered_children = {}
      for child_key, child in self.children.items():
        rendered_children.update({child_key: child.render(mode=mode)})

      return rendered_children

    return self.value

  def empty(self):
    return self.render(mode=modes.FULL)
