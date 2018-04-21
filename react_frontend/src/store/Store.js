
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';
import { createLogger } from 'redux-logger'

import websocketControllerSaga from 'components/abstract/WebsocketController/WebsocketController.saga';
import Reducer from './Reducer';

const logger = createLogger({

});

const sagaMiddleware = createSagaMiddleware();

const Store = createStore(
  Reducer,
  applyMiddleware(
    logger,
    sagaMiddleware,
  ),
);

sagaMiddleware.run(websocketControllerSaga);

export default Store;
