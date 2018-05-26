
import { put, takeLatest } from 'redux-saga/effects';

import { websocketActionCreators, websocketConstants } from 'components/abstract/Websocket';
import APIConstants from '../constants';
import APIActionCreators from './API.actions';

export function* websocketToAPI (action) {
  const {
    socket,
    context: { authentication, authorization, message },
    data: { schema, models, references },
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
    yield put(APIActionCreators.onAPIModelsReceived(socket, message, models));
  }

  if (references) {
    yield put(APIActionCreators.onAPIReferencesReceived(socket, message, references));
  }
}

export function* APIAuthentication (action) {
  const { api, authentication } = action.payload;
  // authentication completed
  // authentication failed

}

function* APISaga () {
  yield takeLatest(websocketConstants.WEBSOCKET_RECEIVE, websocketToAPI);
  yield takeLatest(APIConstants.API_AUTHENTICATION_RECEIVED, APIAuthentication);
}

export default APISaga;
