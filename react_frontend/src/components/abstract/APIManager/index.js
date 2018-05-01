
import { combineReducers } from 'redux';

import APIManagerReducer from './APIManager.reducer';
import APIManager from './APIManager.state';
import APIManagerActionCreators from './APIManager.actions';

const combinedAPIReducer = combineReducers({
  status: APIManagerReducer,
});

export {
  APIManagerActionCreators,
  combinedAPIReducer,
};

export default APIManager;
