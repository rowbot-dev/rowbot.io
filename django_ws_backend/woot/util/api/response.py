
from util.merge import merge

from .modes import modes

class Response():
  _errors = '_errors'
  _value = '_value'
  _description = '_description'
  _server_types = '_server_types'

  def __init__(self, description=None, server_types=None, mode=modes.NORMAL):
    self.description = description
    self.server_types = server_types
    self.mode = mode
    self.value = None
    self.errors = []
    self.children = {}

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
          rendered_response.update({self._errors: self.render_errors()})

        if self.value or self.children:
          rendered_response.update({self._value: self.render_value(mode)})

        return rendered_response

      if self.errors:
        return {self._errors: self.render_errors()}

      if self.value or self.children:
        return self.render_value(mode)

  def render_description_and_types(self, mode):
    if mode.value >= modes.VERBOSE.value:
      return {
        self._description: self.description,
        self._server_types: {_type._type: _type.description for _type in self.server_types},
      }

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
