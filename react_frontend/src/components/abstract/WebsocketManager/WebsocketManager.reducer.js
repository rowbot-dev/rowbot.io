
import { merge } from 'lodash';

import constants from 'store/constants';

const websocketManagerReducer = (state={}, action) => {
  switch (action.type) {
    case constants.WEBSOCKET_OPEN: {
      const { socket, target } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            target,
            open: false,
            reopen: false,
            opening: true,
            closing: false,
            closed: true,
          },
        },
      );
    }
    case constants.WEBSOCKET_OPENED: {
      const { socket } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            open: true,
            reopen: false,
            opening: false,
            closing: false,
            closed: false,
          },
        },
      );
    }
    case constants.WEBSOCKET_CLOSE: {
      const { socket } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            reopen: false,
            opening: false,
            closing: true,
            closed: false,
          },
        },
      );
    }
    case constants.WEBSOCKET_CLOSED: {
      const { socket, reopen } = action.payload;

      return merge(
        {},
        state,
        {
          [socket]: {
            open: false,
            reopen,
            opening: false,
            closing: false,
            closed: true,
          },
        },
      );
    }
    default:
      return state;
  }
}

export default websocketManagerReducer;
