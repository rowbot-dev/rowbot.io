
import constants from 'store/constants';

const withAPIActionCreators = {
  onAPIConsumerRegister: (api, consumer) => ({
    type: constants.API_CONSUMER_REGISTER,
    payload: { api, consumer },
  }),
  onAPIConsumerSetParameters: (api, consumer, parameters) => ({
    type: constants.API_CONSUMER_SET_PARAMETERS,
    payload: { api, consumer, parameters },
  }),
};

export default withAPIActionCreators;
