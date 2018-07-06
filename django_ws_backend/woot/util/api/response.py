
from util.merge import merge

from .constants import constants

class Response():
  def __init__(self, description=None, server_types=None):
    self.description = description
    self.server_types = server_types
    self.active_server_type = None
    self.errors = []
    self.is_empty = False
    self.value = None
    self.rendered = None

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
    }
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
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = {}

  def add_child(self, child_key, child_response):
    self.children.update({child_key: child_response})

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
    }

class ArrayResponse(Response):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.template = None
    self.children = []

  def add_child(self, child_response):
    self.children.append(child_response)

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.TEMPLATE: self.template.render(),
    })

  def render_value(self):
    self.rendered = [
      child_response.render()
      for child_response in self.children
    ]

class IndexedResponse(Response):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.template = None
    self.children = {}

  def add_child(self, child_index, child_response):
    self.children.update({
      child_index: child_response,
    })

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.TEMPLATE: self.template.render(),
    })

  def render_value(self):
    self.rendered = {
      child_index: child_response.render()
      for child_index, child_response in self.children.items()
    }

class TemplateResponse(Response):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.template = None

  def render_empty(self):
    super().render_empty()
    self.rendered.update({
      constants.TEMPLATE: self.template.render(),
    })

  def render_value(self):
    self.render_empty()
