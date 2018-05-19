
import { put, takeLatest } from 'redux-saga/effects';

import constants from 'store/constants';
import { websocketActionCreators } from 'components/abstract/Websocket';
import APIActionCreators from './API.actions';

export function* websocketToAPI (action) {
  const {
    socket,
    context: { authentication, authorization, message },
    data: { schema, models, reference },
  } = action.payload;

  if (authentication) {
    yield put(APIActionCreators.onAPIAuthenticationReceived(socket, message, authentication));
  }

  if (authorization) {
    yield put(APIActionCreators.onAPIAuthorizationReceived(socket, message, authorization));
  }

  if (schema) {
    yield put(APIActionCreators.onAPISchemaReceived(socket, message, schema));
  }

  if (models) {

  }

  // websocket closed from server

  // yield put(APIActionCreators.onAPIReceive(socket, ));
}

export function* APIAuthentication (action) {
  const { api, authentication } = action.payload;
  // authentication completed
  // authentication failed

}

function* APISaga () {
  yield takeLatest(constants.WEBSOCKET_RECEIVE, websocketToAPI);
  yield takeLatest(constants.API_AUTHENTICATION_RECEIVED, APIAuthentication);
}

export default APISaga;
