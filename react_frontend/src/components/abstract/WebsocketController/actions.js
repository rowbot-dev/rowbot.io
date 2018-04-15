
import constants from 'store/constants';
import websocketControllerConstants from './constants';

const websocketControllerActionCreators = {
  openWebsocket: (socket, credentials) => ({
    type: constants.WEBSOCKET_OPEN,
    payload: { socket, credentials },
  }),

  openWebsocketSuccess: (socket, response) => ({
    type: constants.WEBSOCKET_OPEN_SUCCESS,
    payload: { socket, response },
  }),

  openWebsocketFailure: (socket, error) => ({
    type: constants.WEBSOCKET_OPEN_FAILURE,
    payload: { socket, error },
  }),

  sendWebsocketMessage: (socket, id, message) => ({
    type: constants.WEBSOCKET_SEND,
    payload: { socket, id, message },
  }),

  sendWebsocketMessageSuccess: (socket, id, message) => ({
    type: constants.WEBSOCKET_SEND_SUCCESS,
    payload: { socket, id, message },
  }),

  sendWebsocketMessageFailure: (socket, id, error) => ({
    type: constants.WEBSOCKET_SEND_FAILURE,
    payload: { socket, id, error },
  }),

  receiveWebsocketMessage: (socket, id, data) => ({
    type: constants.WEBSOCKET_RECEIVE,
    payload: { socket, id, data },
  }),

  receiveWebsocketMessageSuccess: (socket, id, data) => ({
    type: constants.WEBSOCKET_RECEIVE_SUCCESS,
    payload: { socket, id, data },
  }),

  receiveWebsocketMessageFailure: (socket, id, error) => ({
    type: constants.WEBSOCKET_RECEIVE_FAILURE,
    payload: { socket, id, error },
  }),

  closeWebsocket: socket => ({
    type: constants.WEBSOCKET_CLOSE,
    payload: socket,
  }),

  websocketError: (socket, error) => ({
    type: constants.WEBSOCKET_ERROR,
    payload: { socket, error },
  }),
};

export default websocketControllerActionCreators;
