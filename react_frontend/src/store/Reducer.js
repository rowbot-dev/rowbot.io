
import { combineReducers } from 'redux';

import { combinedWebsocketReducer } from 'components/abstract/WebsocketManager';
import { combinedAPIReducer } from 'components/abstract/APIManager';

const Reducer = combineReducers({
  websockets: combinedWebsocketReducer,
  api: combinedAPIReducer,
});

export default Reducer;
