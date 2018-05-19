
import { combineReducers } from 'redux';

import { websocketReducer } from 'components/abstract/Websocket';
import { APIReducer } from 'components/abstract/API';

const Reducer = combineReducers({
  websockets: websocketReducer,
  api: APIReducer,
});

export default Reducer;
