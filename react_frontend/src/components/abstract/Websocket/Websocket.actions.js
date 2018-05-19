
import constants from 'store/constants';

const websocketActionCreators = {
  onWebsocketOpen: socket => ({
    type: constants.WEBSOCKET_OPENED,
    payload: { socket },
  }),
  onWebsocketRegister: (socket, message, data) => ({
    type: constants.WEBSOCKET_REGISTER,
    payload: { socket, message, data },
  }),
  onWebsocketConsume: socket => ({
    type: constants.WEBSOCKET_CONSUME,
    payload: { socket },
  }),
  onWebsocketReceive: (socket, data, context) => ({
    type: constants.WEBSOCKET_RECEIVE,
    payload: { socket, data, context },
  }),
  onWebsocketClose: (socket, reopen) => ({
    type: constants.WEBSOCKET_CLOSED,
    payload: { socket, reopen },
  }),
  onWebsocketError: (socket, error) => ({
    type: constants.WEBSOCKET_ERROR,
    payload: { socket, error },
  }),
};

export default websocketActionCreators;
