
from util.merge import merge

from .constants import constants
from .errors import errors

class Response():
  def __init__(self, parent_schema):
    self.parent_schema = parent_schema
    self.description = parent_schema.description
    self.server_types = parent_schema.server_types
    self.client_schema = parent_schema.client
    self.active_server_type = None
    self.errors = []
    self.is_empty = False
    self.value = None
    self.rendered = None
    self.has_child_errors = False
    self.should_render = True

  def has_errors(self):
    return self.errors or self.has_child_errors

  def add_error(self, error):
    self.errors.append(error)

  def add_value(self, value):
    self.value = value

  def render(self):
    if self.is_empty:
      self.render_empty()
      return self.rendered

    if self.errors:
      self.render_errors()
      return self.rendered

    self.render_value()
    return self.rendered

  def render_empty(self):
    self.rendered = {
      constants.DESCRIPTION: self.description,
      constants.SERVER_TYPES: {
        server_type.code: server_type.render()
        for server_type in self.server_types
      },
      constants.ERRORS: {
        error.code: error.render()
        for error in self.parent_schema.available_errors
      },
    }

    if self.client_schema is not None:
      self.rendered.update({
        constants.CLIENT: self.client_schema.respond().render(),
      })

    return self.rendered

  def render_errors(self):
    self.rendered = {
      constants.ERRORS: {
        error.code: error.render()
        for error in self.errors
      },
    }
    return self.rendered

  def render_value(self):
    self.rendered = self.value
    return self.rendered

class StructureResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.children = {}

  def add_child(self, child_key, child_response):
    self.children.update({child_key: child_response})

  def get_child(self, child_key):
    return self.children.get(child_key)

  def force_get_child(self, child_key):
    if child_key not in self.children:
      self.add_child(child_key, self.parent_schema.children.get(child_key).get_response())

    return self.get_child(child_key)

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.CHILDREN: {
        child_key: child_response.render()
        for child_key, child_response in self.children.items()
      },
    })

  def render_value(self):
    self.rendered = {
      child_key: child_response.render()
      for child_key, child_response in self.children.items()
      if child_response.should_render
    }

class ArrayResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.template_schema = parent_schema.template
    self.children = []

  def add_child(self, child_response):
    self.children.append(child_response)

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.TEMPLATE: self.template_schema.respond().render(),
    })

  def render_value(self):
    self.rendered = [
      child_response.render()
      for child_response in self.children
    ]

class IndexedResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.template_schema = parent_schema.template
    self.children = {}

  def add_child(self, child_index, child_response):
    self.children.update({
      child_index: child_response,
    })

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.TEMPLATE: self.template_schema.respond().render(),
    })

  def render_value(self):
    self.rendered = {
      child_index: child_response.render()
      for child_index, child_response in self.children.items()
    }

class TemplateResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.template_schema = parent_schema.template

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.TEMPLATE: self.template_schema.respond().render(),
    })

  def render_value(self):
    self.render_empty()
