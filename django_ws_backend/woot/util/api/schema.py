
from util.merge import merge
from .constants import constants
from .modes import modes
from .types import types
from .entry import Entry
from .response import Response

class Schema():

  def __init__(self, models, system_information):
    self.root = Entry({
      'description': 'This schema is a summary of the capabilities of the API',
      'server': types.STRUCTURE('The schema must be present in the client message in some form'),
      'client': types.STRUCTURE('The server message will contain a valid schema'),
      'children': {
        'glossary': Entry({
          'mode': modes.FULL,
          'description': 'A glossary of terms used in the API',
          'server': [
            types.BOOLEAN('Include the whole glossary'),
            types.STRUCTURE('Specify parts of the glossary to include'),
          ],
          'client': types.STRUCTURE('The included glossary'),
          'children': {

          },
        }),
        'types': Entry({
          'mode': modes.VERBOSE,
          'description': 'Variable types used in the API. Client applications should implement relevant validators.',
          'server': [
            types.BOOLEAN('Include all types'),
            types.STRUCTURE('Specify types to include'),
          ],
          'client': types.STRUCTURE('The included types'),
          'children': types.as_entries(),
        }),
        'modes': Entry({
          'mode': modes.VERBOSE,
          'server': types.IMMUTABLE('Modes cannot be modified'),
          'client': types.INTEGER('Modes are represented by a single number'),
          'children': {
            'full': 3,
            'verbose': 2,
            'normal': 1,
            'tiny': 0,
          },
        }),
        'mode': Entry({
          'description': 'The mode of operation of the next interaction with the system',
          'server': types.ENUM(
            modes.FULL,
            modes.VERBOSE,
            modes.NORMAL,
            modes.TINY,
          ),
          'client': types.INTEGER(''),
        }),
        'system': Entry({
          'description': 'Immutable system information, including system models.',
          'server': [
            types.BOOLEAN('Include all system information'),
            types.STRUCTURE('Specify system information to include'),
          ],
          'client': types.STRUCTURE('The included system information'),
          'children': {
            'id': Entry({
              'description': 'The unique ID of the system',
              'server': types.BOOLEAN('Set to true to include id'),
              'client': types.UUID(''),
            }),
            'name': Entry({
              'description': 'The machine-friendly name of the system',
              'server': types.BOOLEAN('Set to true to include name'),
              'client': types.STRING(''),
            }),
            'apiVersion': Entry({
              'description': 'The current API version',
              'server': types.BOOLEAN('Set to true to include the API version'),
              'client': types.STRING(''),
            }),
            'verboseName': Entry({
              'description': 'The verbose name of the system',
              'server': types.BOOLEAN('Set to true to include the verbose name'),
              'client': types.STRING(''),
            }),
            'releaseHash': Entry({
              'description': 'The release hash of the system',
              'server': types.BOOLEAN('Set to true to include the release hash'),
              'client': types.STRING(''),
            }),
            'models': Entry({
              'description': 'Models that fulfill system-related roles, such as user or permission management.',
              'server': [
                types.BOOLEAN('Set to true to include all system models'),
                types.STRUCTURE('Specify system models to include'),
              ],
              'client': types.STRUCTURE('The included system model information'),
              'children': models.as_system_model_entries(),
            }),
          },
        }),
        'context': Entry({
          'description': 'Immutable system information, including system models.',
          'server': [
            types.BOOLEAN('Include all system information'),
            types.STRUCTURE('Specify system information to include'),
          ],
          'client': types.STRUCTURE('The included system information'),
          'children': {
            'client_time_sent': Entry({
              'description': 'The client time at which the message was sent',
              'server': types.TIME(),
              'client': types.TIME(),
            }),
            'server_time_received': Entry({
              'description': 'The server time at which the message was received',
              'server': types.IMMUTABLE(),
              'client': types.TIME(),
            }),
            'query_duration': Entry({
              'description': 'The duration of the last query',
              'server': types.IMMUTABLE(),
              'client': types.INTEGER(),
            }),
            'locale': Entry({
              'description': 'The locale of the client',
              'server': types.STRING(),
              'client': types.STRING(),
            }),
          },
        }),
        'models': Entry({
          'description': 'Persistent data available on the system. A CRUD interface for interacting with stored data.',
          'server': types.STRUCTURE('Queries must be made to specific models'),
          'client': types.STRUCTURE('Structure containing model query results'),
          'children': models.as_entries(),
        }),
      },
    })

  def query(self, payload):
    # create response
    response = self.root.query(payload)

    # extract mode
    mode = response.children.get('mode').get_value(default=modes.NORMAL)

    # render response
    return response.render(mode=mode)
