
import re

from django.db.models import Q

from util.api.errors import Error
from util.random_string import random_string

class CompositeComponentsXNORFailedError(Error):
  pass

class CompositeKeyNotFoundInComponentsError(Error):
  pass

class CompositeInvalidTokenParseError(Error):
  pass

class CompositeInvalidCharacterError(Error):
  pass

class ComponentsInvalidQueryError(Error):
  pass

def recursive_tokeniser(composite):
  composite = re.sub(r'\s+', '', composite)
  tokens = []
  index = 0
  while index < len(composite):
    char = composite[index]
    if char == '(':
      child_tokens, fast_forward = recursive_tokeniser(composite[index+1:])
      index += fast_forward + 1
      tokens.append(child_tokens)
    elif char == ')':
      return tokens, index + 1
    else:
      index += 1
      if tokens:
        if isinstance(tokens[-1], list):
          tokens.append(char)
        else:
          tokens[-1] += char
      else:
        tokens = [char]

  return tokens, index + 1

def composite_parse(composite, components):
  composite_tokens, _ = recursive_tokeniser(composite)
  print(composite_tokens)

  # for component, component_parts in components.items():
  #   key = component_parts.get('_key')
  #   value = component_parts.get('_value')
  #   composite = re.sub(component, 'Q({}="{}")'.format(key, value), composite)
  #
  # filter_query = eval(composite)
  # print(filter_query)

  # top_level_string, nested = composite_parse(composite)
  #
  # print(top_level_string, nested)

  # top_level_string = ''
  # tokens = {}
  # active_token = ''
  # nested_token = ''
  # nested_count = 0
  # length = len(composite)
  # for i, char in enumerate(composite):
  #   nested_count += change(char)
  #
  #   if nested_count:
  #     if active_token:
  #       top_level_string += active_token
  #       active_token = ''
  #     else:
  #       nested_token += char
  #   else:
  #     if nested_token:
  #       key = random_string(8)
  #       tokens.update({key: nested_token})
  #       top_level_string += key
  #       nested_token = ''
  #     else:
  #       if i == length - 1:
  #         top_level_string += active_token + composite[-1]
  #       else:
  #         active_token += char
  #
  # base_query = Q()
  # for and_group in top_level_string.split('|'):
  #   and_query = Q()
  #   for token in and_group.split('&'):
  #     token_string = token.strip()
  #     if token_string:
  #       N = False
  #       if token_string[0] == '~':
  #         N = True
  #         token_string = token_string[1:]
  #
  #       if token_string in tokens:
  #         nested_token = tokens.get(token_string)
  #         # if nested_token[0] == '(':
  #         #   nested_token = nested_token[1:]
  #         if nested_token[-1] == ')':
  #           nested_token = nested_token[:-1]
  #
  #         print(nested_token, recursive_composite_parse(nested_token, components))
  #         and_query = and_query & recursive_composite_parse(nested_token, components)
  #       elif token_string in components:
  #         key = components.get(token_string).get('_key')
  #         value = components.get(token_string).get('_value')
  #
  #         if N:
  #           and_query = and_query & ~Q(**{key: value})
  #         else:
  #           and_query = and_query & Q(**{key: value})
  #
  #   base_query = base_query | and_query
  #
  # return base_query

def construct_filter_query(composite=None, components=None, sorting=None, pagination=None):
  return None, [], []
