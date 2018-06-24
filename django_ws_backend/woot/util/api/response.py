
from util.merge import merge

class Response():
  def __init__(self, description=None, server_types=None):
    self.description = description
    self.server_types = server_types
    self.value = None
    self.errors = []
    self.children = {}

  def add_error(self, error):
    self.errors.append(error)

  def add_child(self, child_name, child):
    self.children.update({child_name: child})

  def add_value(self, value):
    self.value = value

  def render(self):
    rendered_response = self.render_mode_dependent()

    if rendered_response:
      if self.errors:
        rendered_response.update({'_errors': self.render_errors()})

      if self.value or self.children:
        rendered_response.update({'_value': self.render_value()})

      return rendered_response

    if self.errors:
      return {'_errors': self.render_errors()}

    if self.value or self.children:
      return self.render_value()

  def render_mode_dependent(self):
    return {}

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

    return self.value
