
import constants from 'store/constants';
import websocketControllerConstants from './constants';

const websocketControllerActionCreators = {
  connectToWebsocket: credentials => ({
    type: constants.WEBSOCKET_CONNECT,
    payload: credentials,
  }),

  connectToWebsocketSuccess: response => ({
    type: constants.WEBSOCKET_CONNECT_SUCCESS,
    payload: response,
  }),

  connectToWebsocketFailure: error => ({
    type: constants.WEBSOCKET_CONNECT_FAILURE,
    payload: error,
  }),

  sendWebsocketMessage: message => ({
    type: constants.WEBSOCKET_SEND,
    payload: message,
  }),

  sendWebsocketMessageSuccess: message => ({
    type: constants.WEBSOCKET_SEND_SUCCESS,
    payload: message,
  }),

  sendWebsocketMessageFailure: message => ({
    type: constants.WEBSOCKET_SEND_FAILURE,
    payload: message,
  }),

  receiveWebsocketMessage: message => ({
    type: constants.WEBSOCKET_RECEIVE,
    payload: message,
  }),

  receiveWebsocketMessageSuccess: response => ({
    type: constants.WEBSOCKET_RECEIVE_SUCCESS,
    payload: response,
  }),

  receiveWebsocketMessageFailure: error => ({
    type: constants.WEBSOCKET_RECEIVE_FAILURE,
    payload: error,
  }),
};

export default websocketControllerActionCreators;
