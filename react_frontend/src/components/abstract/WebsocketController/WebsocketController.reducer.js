
import { merge } from 'lodash';

import constants from 'store/constants';

const websocketControllerReducer = (state={}, action) => {
  switch (action.type) {
    case constants.WEBSOCKET_OPEN: {
      const { socket } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            open: true,
            messages: {},
            active: null,
          }
        },
      );
    }
    case constants.WEBSOCKET_SEND: {
      const { socket, id, message } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            messages: {
              [id]: { message },
            },
          },
        },
      );
    }
    case constants.WEBSOCKET_CONSUME: {
      const { socket } = action.payload;
      const { messages = {} } = (state[socket] || {});
      const [ id, ...rest ] = Object.keys(messages);

      return merge(
        {},
        state,
        {
          [socket]: { active: id },
        },
      );
    }
    case constants.WEBSOCKET_CONSUME_SUCCESS: {
      const { socket, id } = action.payload;

      let newState = merge({}, state);
      delete newState[socket].messages[id];
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

export default websocketControllerReducer;
