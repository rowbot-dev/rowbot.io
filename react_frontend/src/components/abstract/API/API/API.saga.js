
import { put, takeLatest } from 'redux-saga/effects';

import constants from 'store/constants';
import { websocketActionCreators } from 'components/abstract/Websocket';
import APIActionCreators from './API.actions';

export function* websocketToAPI (action) {
  const {
    socket,
    data: { schema, models },
    context: { authentication },
  } = action.payload;

  if (schema) {
    yield put(APIActionCreators.onAPISchemaReceived(socket, schema));
  }

  if (authentication) {
    yield put(APIActionCreators.onAPIAuthenticationReceived(socket, authentication));
  }

  // authentication completed
  // authentication failed
  // websocket closed from server

  // yield put(APIActionCreators.onAPIReceive(socket, ));
}

export function* APIAuthentication (action) {
  const { api, authentication } = action.payload;


}

function* APISaga () {
  yield takeLatest(constants.WEBSOCKET_RECEIVE, websocketToAPI);
  yield takeLatest(constants.API_AUTHENTICATION_RECEIVED, APIAuthentication);
}

export default APISaga;
