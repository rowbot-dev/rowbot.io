
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';

import Reducer from './Reducer';
import websocketControllerReducer from 'components/abstract/WebsocketController/Reducer';

import websocketControllerSaga from 'components/abstract/WebsocketController/Saga';

const sagaMiddleware = createSagaMiddleware();

const Store = createStore(
  Reducer,
  applyMiddleware(
    sagaMiddleware,
  ),
);

sagaMiddleware.run(websocketControllerSaga);

export default Store;
