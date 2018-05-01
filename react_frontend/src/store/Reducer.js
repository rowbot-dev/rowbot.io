
import { combineReducers } from 'redux';

import { combinedWebsocketReducer } from 'components/abstract/WebsocketManager';
import { combinedAPIReducer } from 'components/abstract/APIManager';

const Reducer = combineReducers({
  api: combinedAPIReducer,
  websockets: combinedWebsocketReducer,
});

export default Reducer;
