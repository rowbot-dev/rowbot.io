
import uuid from 'util/uuid';
import constants from 'store/constants';
// import websocketControllerConstants from './WebsocketController.constants';

const websocketControllerActionCreators = {
  openWebsocket: (socket, credentials) => ({
    type: constants.WEBSOCKET_OPEN,
    payload: { socket, credentials },
  }),

  sendWebsocketMessage: (socket, id, message) => ({
    type: constants.WEBSOCKET_SEND,
    payload: { socket, id, message },
  }),

  consumeWebsocketMessage: socket => ({
    type: constants.WEBSOCKET_CONSUME,
    payload: { socket },
  }),

  consumeWebsocketMessageSuccess: (socket, id) => ({
    type: constants.WEBSOCKET_CONSUME_SUCCESS,
    payload: { socket, id },
  }),

  receiveWebsocketMessage: (socket, id, data) => ({
    type: constants.WEBSOCKET_RECEIVE,
    payload: { socket, id, data },
  }),

  closeWebsocket: socket => ({
    type: constants.WEBSOCKET_CLOSE,
    payload: socket,
  }),

  websocketError: (socket, message, error) => ({
    type: constants.WEBSOCKET_ERROR,
    payload: { socket, message, error },
  }),
};

export default websocketControllerActionCreators;
