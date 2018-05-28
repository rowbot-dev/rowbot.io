
import { merge } from 'lodash';

import constants from './API.constants';

const APIReducer = (state = {}, action) => {
  switch (action.type) {
    case constants.API_CREATE: {
      const { api, target } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            status: {
              target,
              created: false,
              creating: true,
              destroying: false,
              destroyed: true,
            },
          },
        },
      );
    }
    case constants.API_CREATED: {
      const { api } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            authentication: {
              pending: true,
              completed: false,
            },
            status: {
              created: true,
              creating: false,
              destroying: false,
              destroyed: false,
            },
          },
        },
      );
    }
    case constants.API_SCHEMA_RECEIVED: {
      const { api, schema } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            data: { schema },
          },
        },
      );
    }
    case constants.API_QUERY: {
      const { api } = action.payload;

      return state;
    }
    case constants.API_RECEIVE: {
      const { api } = action.payload;

      return state;
    }
    case constants.API_DESTROY: {
      const { api } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            status: {
              created: true,
              creating: false,
              destroying: true,
              destroyed: false,
            },
          },
        },
      );
    }
    case constants.API_DESTROYED: {
      const { api } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            status: {
              target: null,
              created: false,
              creating: false,
              destroying: false,
              destroyed: true,
            },
          },
        },
      );
    }
    case constants.API_CONSUMER_REGISTER: {
      const { api, consumer } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            consumers: {
              [consumer]: {
                references: {},
              },
            },
          },
        },
      );
    }
    case constants.API_CONSUMER_CONFIRM_SENDER_VALUE: {
      const { api, consumer, sender } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            senders: {
              [sender]: {
                consumers: {
                  [consumer]: true,
                },
              },
            },
          },
        },
      );
    }
    case constants.API_CONSUMER_ADD_REFERENCE: {
      const { api, consumer, identifier, query } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            consumers: {
              [consumer]: {
                references: {
                  [identifier]: {
                    query,
                    local: false,
                    remote: false,
                  },
                },
              },
            },
          },
        },
      );
    }
    case constants.API_CONSUMER_CONSUME_REFERENCE: {
      const { api, consumer, identifier } = action.payload;
      const {
        [api]: {
          consumers: {
            [consumer]: {
              references: {
                [identifier]: discardedReference,
                ...otherReferences
              },
              ...restOfConsumer
            },
            ...otherConsumers
          },
          ...restOfAPI
        },
        ...otherAPIs
      } = state;

      return {
        [api]: {
          consumers: {
            [consumer]: {
              references: otherReferences,
              ...restOfConsumer,
            },
            ...otherConsumers,
          },
          ...restOfAPI,
        },
        ...otherAPIs,
      };
    }
    case constants.API_SENDER_REGISTER: {
      const { api, sender } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            senders: {
              [sender]: {
                value: null,
              },
            },
          },
        },
      );
    }
    case constants.API_SENDER_SET_VALUE: {
      const { api, sender, value } = action.payload;

      const {
        [api]: {
          senders: {
            [sender]: discardedSender,
            ...otherSenders
          },
          ...restOfAPI
        },
        ...otherAPIs
      } = state;

      return {
        [api]: {
          senders: {
            [sender]: {
              value,
            },
            ...otherSenders,
          },
          ...restOfAPI,
        },
        ...otherAPIs,
      };
    }
    default:
      return state;
  }
};

export default APIReducer;
