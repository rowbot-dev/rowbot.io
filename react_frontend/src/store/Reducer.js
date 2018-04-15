
import { combineReducers } from 'redux';

import websocketControllerReducer from 'components/abstract/WebsocketController/Reducer';

const Reducer = combineReducers({
  websockets: websocketControllerReducer,
});

export default Reducer;
