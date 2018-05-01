
import { combineReducers } from 'redux';

import websocketManagerReducer from './WebsocketManager.reducer';
import WebsocketManager from './WebsocketManager.state';
import websocketManagerActionCreators from './WebsocketManager.actions';

import websocketReducer from './Websocket/Websocket.reducer';
import websocketActionCreators from './Websocket/Websocket.actions';
import { websocketDataSelector } from './Websocket/Websocket.selectors';

const combinedWebsocketReducer = combineReducers({
  status: websocketManagerReducer,
  data: websocketReducer,
});

export {
  websocketManagerActionCreators,
  websocketActionCreators,
  websocketDataSelector,
  combinedWebsocketReducer,
};

export default WebsocketManager;
