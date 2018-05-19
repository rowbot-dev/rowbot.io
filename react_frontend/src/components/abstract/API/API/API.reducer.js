
import { merge } from 'lodash';

import constants from 'store/constants';

const APIReducer = (state={}, action) => {
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
            data: {
              schema: {},
              authentication: {
                pending: true,
                completed: false,
              },
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
    case constants.API_AUTHENTICATION_BEGIN: {
      const { api } = action.payload;

      return state;
    }
    case constants.API_AUTHENTICATION_COMPLETED: {
      const { api } = action.payload;

      return state;
    }
    case constants.API_AUTHENTICATION_FAILED: {
      const { api } = action.payload;

      return state;
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
    default:
      return state;
  }
}

export default APIReducer;
