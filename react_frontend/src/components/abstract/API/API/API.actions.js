
import constants from '../API.constants';

const APIActionCreators = {
  onAPICreated: api => ({
    type: constants.API_CREATED,
    payload: { api },
  }),
  onAPIAuthorizationReceived: (api, message, authorization) => ({
    type: constants.API_AUTHORIZATION_RECEIVED,
    payload: { api, message, authorization },
  }),
  onAPIAuthenticationReceived: (api, message, authentication) => ({
    type: constants.API_AUTHENTICATION_RECEIVED,
    payload: { api, message, authentication },
  }),
  onAPISchemaReceived: (api, message, schema) => ({
    type: constants.API_SCHEMA_RECEIVED,
    payload: { api, message, schema },
  }),
  onAPIModelsReceived: (api, message, models) => ({
    type: constants.API_MODELS_RECEIVED,
    payload: { api, message, models },
  }),
  onAPIReferencesReceived: (api, message, references) => ({
    type: constants.API_REFERENCES_RECEIVED,
    payload: { api, message, references },
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
