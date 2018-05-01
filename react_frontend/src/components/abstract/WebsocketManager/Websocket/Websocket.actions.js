
import uuid from 'util/uuid';
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
  onWebsocketReceive: (socket, message, data) => ({
    type: constants.WEBSOCKET_RECEIVE,
    payload: { socket, message, data },
  }),
  onWebsocketClose: (socket, reopen) => ({
    type: constants.WEBSOCKET_CLOSED,
    payload: { socket, reopen },
  }),
  onWebsocketError: (socket, message, error) => ({
    type: constants.WEBSOCKET_ERROR,
    payload: { socket, message, error },
  }),
};

export default websocketActionCreators;
