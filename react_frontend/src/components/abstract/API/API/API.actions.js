
import constants from 'store/constants';

const APIActionCreators = {
  onAPICreated: api => ({
    type: constants.API_CREATED,
    payload: { api },
  }),
  onAPISchemaReceived: (api, schema) => ({
    type: constants.API_SCHEMA_RECEIVED,
    payload: { api, schema },
  }),
  onAPIAuthenticationReceived: (api, authentication) => ({
    type: constants.API_AUTHENTICATION_RECEIVED,
    payload: { api, authentication },
  }),
  onAPIAuthenticationBegin: api => ({
    type: constants.API_AUTHENTICATION_BEGIN,
    payload: { api },
  }),
  onAPIAuthenticationCompleted: api => ({
    type: constants.API_AUTHENTICATION_COMPLETED,
    payload: { api },
  }),
  onAPIAuthenticationFailed: api => ({
    type: constants.API_AUTHENTICATION_FAILED,
    payload: { api },
  }),
  onAPIQuery: (api, model, query) => ({
    type: constants.API_QUERY,
    payload: { api, model, query },
  }),
  onAPIReceive: (api, model, data) => ({
    type: constants.API_RECEIVE,
    payload: { api, model, data },
  }),
  onAPIDestroyed: api => ({
    type: constants.API_DESTROYED,
    payload: { api },
  }),
};

export default APIActionCreators;
