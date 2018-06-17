
from util.merge import merge

class modes:
  FULL = 3
  VERBOSE = 2
  NORMAL = 1
  TINY = 0

class constants:
  TEMPLATE = '_template'

class types:
  BOOLEAN = '__boolean'

class Entry():
  def __init__(self):

def pick(level, verbosity, structure):
  if level >= verbosity:
    return structure
  return {}

class Schema():

  def __init__(self, models, system_information, payload, mode=modes.NORMAL):
    self.models = models
    self.system_information = system_information
    self.payload = payload
    self.check_payload_successful = False
    self.check_authentication_process_successful = False

    self.get_context(mode)

  def get_context(self, mode):
    payload = self.payload if self.payload is not None else {}
    context = payload.get('context', {})
    self.mode = context.get('mode', mode)
    self.authorization = context.get('authorization')

  def check_payload(self):
    payload = self.payload if self.payload is not None else {}
    self.render_for_payload_check()
    self.check_payload_successful = recursive_data_check(self.payload_check_render, payload)

  def recursive_data_check(self, template, data, key=None):
    if isinstance(template, dict) and isinstance(data, dict):
      # if there is a '_key' key, type-check the key
      # if there is a '_type' key, iterate through it and check the corresponding value against each type
      # if there is a '_values' key, iterate through it and check the value against each one
      # if there are none of these keys, go down to the next level

  def render_for_payload_check(self):
    self.payload_check_render = merge(
      {
        'context': merge(
          pick(self.mode, modes.VERBOSE, {
            '_description': 'The context of the request or response contains query-specific identifiers such as UUIDs, timestamps, and hashes.',
          }),
          {
            'mode': merge(
              pick(self.mode, modes.VERBOSE, {
                '_description': 'The level of detail in the schema',
              }),
              {
                '_type': '__string',
                '_values': {
                  'full': 'Returns this entire schema including the top-level info key and all description keys, even if the keys are not relevant to the current request or response.',
                  'verbose': 'Keeps the description keys, but not the info keys.',
                  'normal': 'Removes all description keys and keys not relevant to the request, and moves keys inside request or response to the top level.',
                  'tiny': 'Removes all structure including the context when possible. This should only be used to return simple information such as a single value when the endpoint of the response is known.',
                },
              },
            ),
            'authorization': merge(
              pick(self.mode, modes.VERBOSE, {
                '_description': 'An authorization token to be included with each request. It is the primary key of an authorization token object on the system.',
              }),
              {
                '_type': '__uuid',
              },
            ),
          },
        ),
        'query': merge(
          pick(self.mode, modes.VERBOSE, {
            '_description': 'All queries made to the API must be of this form. Only keys relevant to the query should be included. Any request that does not contain a valid subset of this structure will be rejected with an explicit error.',
          }),
          {
            'time': merge(
              pick(self.mode, modes.VERBOSE, {
                '_description': 'The timestamp of the request from the client side',
              }),
              {
                'location': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The location of the sender',
                  }),
                  {
                    '_type': '__string',
                  },
                ),
                'locale': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The locale of the sender',
                  }),
                  {
                    '_type': '__string',
                  },
                ),
                'timestamp': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The time the request left the client',
                  }),
                  {
                    '_type': '__time',
                  },
                ),
              },
            ),
            'system': merge(
              pick(self.mode, modes.VERBOSE, {
                '_description': 'A set of information about the system that the server is running, including version information.',
              }),
              {
                '_type': {
                  '__boolean': 'Include all system information',
                  '__structure': 'Pick system information to include',
                },
                'id': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The uuid of the API',
                  }),
                  {
                    '_type': '__boolean',
                  },
                ),
                'name': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The name of the API',
                  }),
                  {
                    '_type': '__boolean',
                  },
                ),
                'verboseName': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The verbose name of the API',
                  }),
                  {
                    '_type': '__boolean',
                  },
                ),
                'apiVersion': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The API version of the API',
                  }),
                  {
                    '_type': '__boolean',
                  },
                ),
                'releaseHash': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'The release hash of the API',
                  }),
                  {
                    '_type': '__boolean',
                  },
                ),
                'models': merge(
                  pick(self.mode, modes.VERBOSE, {
                    '_description': 'System models reserved for key functions such as authentication',
                  }),
                  {
                    '_type': {
                      '__boolean': 'Include all system models',
                      '__structure': 'Pick system models to include',
                    },
                    'reference': merge(
                      pick(self.mode, modes.VERBOSE, {
                        '_description': 'A combination of object name and UUID allowing a reference to a single object on the system',
                      }),
                      {
                        '_type': '__boolean',
                      },
                    ),
                    'user': merge(
                      pick(self.mode, modes.VERBOSE, {
                        '_description': 'A unique identity on the system',
                      }),
                      {
                        '_type': '__boolean',
                      },
                    ),
                    'authentication': merge(
                      pick(self.mode, modes.VERBOSE, {
                        '_description': 'A model used to mediate the authentication process',
                      }),
                      {
                        '_type': '__boolean',
                      },
                    ),
                    'authorization': merge(
                      pick(self.mode, modes.VERBOSE, {
                        '_description': 'An authorization token for persistent access control',
                      }),
                      {
                        '_type': '__boolean',
                      },
                    ),
                    'error': merge(
                      pick(self.mode, modes.VERBOSE, {
                        '_description': 'An error reporting model',
                      }),
                      {
                        '_type': '__boolean',
                      },
                    ),
                  },
                ),
              },
            ),
            'models': merge(
              pick(self.mode, modes.VERBOSE, {
                '_description': 'A list of models available on the system',
              }),
              {
                '_template': {
                  '_key': '__model',
                  'attributes': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Non-related object properties of an object. Types and values will be set from the system. During any request, the specified attributes will be included with the response.',
                    }),
                    {
                     '_type': {
                       '__boolean': 'Include all attributes',
                       '__structure': 'Pick attributes to include',
                     },
                     '_template': {
                       '_type': '__boolean',
                     },
                    },
                  ),
                  'relationships': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Related objects referenced via models on the system.',
                    }),
                    {
                      '_template': {
                        '_type': {
                          '__boolean': 'Include the reference to the object if it is singular, else the related model name.',
                          '__structure': 'Add a level of recursion starting from the models _template.',
                        },
                      },
                    },
                  ),
                  'methods': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'A list of models available on the system',
                    }),
                    {
                      '_template': {
                        '_type': {
                          '__boolean': 'Include details of the method',
                          '__structure': 'Call the method with arguments defined by the system',
                        },
                      },
                    },
                  ),
                  'instances': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Instances of the model class. Attributes or relationships to include cannot be specified here.',
                    }),
                    {
                      '_template': {
                        '_key': '__uuid',
                        'update': merge(
                          pick(self.mode, modes.VERBOSE, {
                            '_description': 'Set this key to explicitly update the instance rather than fetching it',
                          }),
                          {
                            '_type': '__boolean',
                          },
                        ),
                        'attributes': {},
                        'methods': merge(
                          pick(self.mode, modes.VERBOSE, {
                            '_description': 'Call methods on a single instance',
                          }),
                          {
                            '_template': {
                              '_type': '__structure',
                            },
                          },
                        ),
                        'relationships': {
                          '_template': {
                            '_type': {
                              '__ref': 'Set a singular relationship',
                              '__array': 'Set multiple related objects',
                            },
                          },
                        },
                      },
                    },
                  ),
                  'filter': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Impose a filter on a model',
                    }),
                    {
                      '_template': merge(
                        pick(self.mode, modes.VERBOSE, {
                          '_description': 'An object containing the information necessary to compose a filter',
                        }),
                        {
                          'composite': merge(
                            pick(self.mode, modes.VERBOSE, {
                              '_description': 'A string of the form A & B | C, or any combination of unitary operators to combine the named components, conforming to Django query notation.',
                            }),
                            {
                              '_type': '__string',
                            },
                          ),
                          'components': merge(
                            pick(self.mode, modes.VERBOSE, {
                              '_description': 'A series of named components in the form related__attributed__directive, conforming to Django query notation.',
                            }),
                            {
                              '_template': {
                                '_type': '__string',
                              },
                            },
                          ),
                        },
                      ),
                    },
                  ),
                  'sort': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Sort instances of a model',
                    }),
                    {
                      '_template': merge(
                        pick(self.mode, modes.VERBOSE, {
                          '_description': 'A string of the form (-)relationship__attribute conforming to Django query notation.',
                        }),
                        {
                          '_type': '__string',
                        },
                      ),
                    },
                  ),
                  'paginate': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Paginate instances of a model',
                    }),
                    {
                      'page': merge(
                        pick(self.mode, modes.VERBOSE, {
                          '_description': 'The current page',
                        }),
                        {
                          '_type': {
                            '__boolean': 'Fetch the current value',
                            '__number': 'Set the current value',
                          },
                        },
                      ),
                      'pages': merge(
                        pick(self.mode, modes.VERBOSE, {
                          '_description': 'The current number of pages',
                        }),
                        {
                          '_type': '__boolean',
                        },
                      ),
                      'size': merge(
                        pick(self.mode, modes.VERBOSE, {
                          '_description': 'The current page size',
                        }),
                        {
                          '_type': {
                            '__boolean': 'Fetch the current page size',
                            '__number': 'Set the current page size',
                          },
                        },
                      ),
                    },
                  ),
                  'create': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Create instances',
                    }),
                    {
                      '_template': merge(
                        pick(self.mode, modes.VERBOSE, {
                          '_description': 'Keys will be the identifier of the new instance',
                        }),
                        {
                          '_key': '__uuid',
                          'identifier': merge(
                            pick(self.mode, modes.VERBOSE, {
                              '_description': 'Each prototype is given a temporary identifier to match it with the newly created object',
                            }),
                            {
                              '_type': '__uuid',
                            },
                          ),
                          'attributes': {},
                          'relationships': {
                            '_template': {
                              '_type': {
                                '__ref': 'A singular related object',
                                '__array': 'Multiple related objects',
                              },
                            },
                          },
                        },
                      ),
                    },
                  ),
                  'delete': merge(
                    pick(self.mode, modes.VERBOSE, {
                      '_description': 'Delete instances',
                    }),
                    {
                      '_template': {
                        '_type': '__uuid',
                      },
                    },
                  ),
                },
              },
            ),
          },
        ),
      },
    )

  def check_authentication_process(self):
    # 1. request to be authenticated
    # 2. request to be re-authenticated
    # 3. return of challenge
    pass

  def render_for_authentication_process(self):
    pass

  def query(self, model_name, query, authorization):
    Model = self.get_model(model_name)

    if Model is None:
      return Errors.no_such_model(model_name)

    return Model.objects.query(query, authorization=authorization)

  def render_for_query(self):
    # 1. get mode and authorization from payload
    payload = self.payload if self.payload is not None else {}
    context = payload.get('context', {})
    mode = context.get('mode', modes.NORMAL)
    authorization = context.get('authorization')

    # 2. generate content based on mode, authorization, models, and system_information
    this.query_render = merge(
      pick(mode, modes.VERBOSE, {
        '_description': 'This schema is a summary of the capabilities of the API. Parts of it are meant to be read by a client built to consume the API, and have a more consistent structure. Any key beginning with "__" is human-readable, and is not meant to be parsed. These keys can be removed by changing the mode in the context. If they are included in the response, they will be ignored.',
      }),
      pick(mode, modes.FULL, {
        '_golossary': {
          '_description': 'Any "_description" key is assumed to be a verbose, human-readable description of the parent key and the structure it contains. If the value of a key is a string, this string is treated as its description.',
          'type': 'Type of data expected to be received or set on the parent key, for purposes of validation.',
          'values': 'In the case of an enum, the different values that the parent key can take.',
          'system': 'The remote server that the API is served from.',
          'request': 'The data structure sent to the system.',
          'query': 'The part of the request concerned with specific data from the system.',
          'response': 'The data structure received from the system.',
          'structure': 'A JSON object consisting of keys, values, arrays, and nested objects.',
          'object': 'A database model or its representation',
          'client': 'The application consuming the API',
          'server': 'The physical machine where the API is running',
          'model': 'The name of the database model on the system',
          'ref': 'A combination of database model name and the UUID of a specific instance, in the form __model.__uuid, to allow it to be unique identified on the system.',
        },
      }),
      pick(mode, modes.FULL, {
        '_types': {
          '_description': 'A simple set of high level validation types to prevent basic errors. These should be implemented by any client application.',
          '__model': 'A database object model name on the system',
          '__structure': 'A JSON object',
          '__array': 'A JSON array',
          '__boolean': 'A true or false value',
          '__number': 'An integer or a floating point value',
          '__string': 'String, but not a uuid, ref, or timestamp',
          '__uuid': 'A valid UUID',
          '__time': 'A valid timestamp',
          '__ref': '__model.__uuid, a reference to a specific object on the system'
        },
      }),
      {

      },
    )

  def render(self):
    pass
