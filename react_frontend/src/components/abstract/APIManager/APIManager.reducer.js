
import { merge } from 'lodash';

import constants from 'store/constants';

const APIManagerReducer = (state={}, action) => {
  switch (action.type) {
    case constants.API_CREATE: {
      const { api, target } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            target,
            created: false,
            creating: true,
            destroying: false,
            destroyed: true,
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
            created: true,
            creating: false,
            destroying: false,
            destroyed: false,
          },
        },
      );
    }
    case constants.API_DESTROY: {
      const { api } = action.payload;

      return merge(
        {},
        state,
        {
          [api]: {
            created: true,
            creating: false,
            destroying: true,
            destroyed: false,
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
            created: false,
            creating: false,
            destroying: false,
            destroyed: true,
          },
        },
      );
    }
    default:
      return state;
  }
}

export default APIManagerReducer;
