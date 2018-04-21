
import { combineReducers } from 'redux';

import websocketControllerReducer from 'components/abstract/WebsocketController/WebsocketController.reducer';

const Reducer = combineReducers({
  websockets: websocketControllerReducer,
});

export default Reducer;
