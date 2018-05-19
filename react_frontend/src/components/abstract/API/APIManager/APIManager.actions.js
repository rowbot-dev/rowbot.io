
import constants from 'store/constants';

const APIManagerActionCreators = {
  createAPI: (api, target) => ({
    type: constants.API_CREATE,
    payload: { api, target },
  }),
  destroyAPI: api => ({
    type: constants.API_DESTROY,
    payload: { api },
  }),
};

export default APIManagerActionCreators;
