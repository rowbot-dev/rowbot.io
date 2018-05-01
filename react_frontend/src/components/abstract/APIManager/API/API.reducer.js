
import { merge } from 'lodash';

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
            messages: {},
            active: null,
          },
        },
      );
    }
    case constants.WEBSOCKET_REGISTER: {
      const { socket, message, data } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            messages: {
              [message]: { data },
            },
          },
        },
      );
    }
    case constants.WEBSOCKET_CONSUME: {
      const { socket } = action.payload;
      const { messages = {} } = (state[socket] || {});
      const [message, ...rest] = Object.keys(messages);

      return merge(
        {},
        state,
        {
          [socket]: { active: message },
        },
      );
    }
    case constants.WEBSOCKET_RECEIVE: {
      const { socket, message } = action.payload;

      let newState = merge({}, state);
      delete newState[socket].messages[message];
      delete newState[socket].active;

      return newState;
    }
    case constants.WEBSOCKET_ERROR: {
      const { socket, message } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: { error: message },
        },
      );
    }
    default:
      return state;
  }
}

export default websocketReducer;
