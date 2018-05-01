
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';
import { createLogger } from 'redux-logger'

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

// sagaMiddleware.run();

export default Store;
