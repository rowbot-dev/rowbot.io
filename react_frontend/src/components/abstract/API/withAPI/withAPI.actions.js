
import constants from '../constants';

const withAPIActionCreators = {
  onAPIConsumerRegister: (api, consumer) => ({
    type: constants.API_CONSUMER_REGISTER,
    payload: { api, consumer },
  }),
  onAPIConsumerReferenceAdd: (api, consumer, identifier, args) => ({
    type: constants.API_CONSUMER_REFERENCE_ADD,
    payload: { api, consumer, identifier, args },
  }),
};

export default withAPIActionCreators;
