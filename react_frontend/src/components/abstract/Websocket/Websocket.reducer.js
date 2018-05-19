
import { merge, mergeWith, isArray, isObject } from 'lodash';

import constants from 'store/constants';

const websocketReducer = (state={}, action) => {
  switch (action.type) {
    case constants.WEBSOCKET_OPENED: {
      const { socket } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            status: {
              open: true,
              reopen: false,
              opening: false,
              closing: false,
              closed: false,
            },
            messages: [],
            active: null,
            consumed: {},
          },
        },
      );
    }
    case constants.WEBSOCKET_REGISTER: {
      const { socket, message, data } = action.payload;

      return mergeWith(
        {},
        state,
        {
          [socket]: {
            messages: [{ id: message, data }],
          }
        },
        (objValue, srcValue) => {
          if (isArray(objValue)) {
            return objValue.concat(srcValue);
          }
        },
      );
    }
    case constants.WEBSOCKET_CONSUME: {
      const { socket } = action.payload;
      const { messages = [] } = (state[socket] || {});
      const [message, ...rest] = messages;
      const { id, data } = message;

      return mergeWith(
        {},
        state,
        {
          [socket]: {
            messages: rest,
            active: id,
            consumed: {
              [id]: data,
            },
          }
        },
        (objValue, srcValue) => {
          if (isArray(objValue)) {
            return srcValue;
          }
        },
      );
    }
    case constants.WEBSOCKET_RECEIVE: {
      const { context: { message } } = action.payload;

      return mergeWith(
        {},
        state,
        (objValue, srcValue) => {
          if (isObject(srcValue) && message && message in srcValue) {
            delete srcValue[message];
            return srcValue;
          }
        }
      );
    }
    case constants.WEBSOCKET_CLOSED: {
      const { socket, reopen } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            status: {
              open: false,
              reopen,
              opening: false,
              closing: false,
              closed: true,
            },
          },
        },
      );
    }
    case constants.WEBSOCKET_ERROR: {
      const { socket, message, error } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: { error: { message, error } },
        },
      );
    }
    default:
      return state;
  }
}

export default websocketReducer;
