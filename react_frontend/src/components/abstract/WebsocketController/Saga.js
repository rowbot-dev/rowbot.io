
import { call, put, takeLatest } from 'redux-saga/effects';

import constants from 'store/constants';
import websocketControllerActionCreators from './actions';
import websocketControllerConstants from './constants';

function* connectToWebsocket (action) {

}

function* sendWebsocketMessage (action) {

}

function* receiveWebsocketMessage (action) {
  
}

function* websocketControllerSaga () {
  yield takeLatest(constants.WEBSOCKET_CONNECT, connectToWebsocket);
  yield takeLatest(constants.WEBSOCKET_MESSAGE_SEND, sendWebsocketMessage);
  yield takeLatest(constants.WEBSOCKET_MESSAGE_RECEIVE, receiveWebsocketMessage);
}

export default websocketControllerSaga;
