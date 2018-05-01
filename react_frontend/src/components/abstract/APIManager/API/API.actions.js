
import constants from 'store/constants';

const APIActionCreators = {
  onAPICreate: api => ({
    type: constants.API_CREATED,
    payload: { api },
  }),
  onAPIDestroy: api => ({
    type: constants.API_DESTROYED,
    payload: { api },
  }),
};

export default APIActionCreators;
