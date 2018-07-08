
query_directive_array = [
  'startswith',
  'contains',
  'icontains',
]

class query_directives:
  JOIN = '__'

for directive in query_directive_array:
  setattr(query_directives, directive.upper(), directive)

def is_valid_query_directive(directive):
  return directive in query_directive_array
