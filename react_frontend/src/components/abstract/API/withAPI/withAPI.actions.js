
import constants from '../API.constants';

const withAPIActionCreators = {
  onAPIConsumerRegister: (api, consumer, senders) => ({
    type: constants.API_CONSUMER_REGISTER,
    payload: { api, consumer, senders },
  }),
  onAPIConsumerConfirmSenderValue: (api, consumer, sender) => ({
    type: constants.API_CONSUMER_CONFIRM_SENDER_VALUE,
    payload: { api, consumer, sender },
  }),
  onAPIConsumerAddReference: (api, consumer, identifier, query) => ({
    type: constants.API_CONSUMER_ADD_REFERENCE,
    payload: { api, consumer, identifier, query },
  }),
  onAPIConsumerConsumeReference: (api, consumer, identifier) => ({
    type: constants.API_CONSUMER_CONSUME_REFERENCE,
    payload: { api, consumer, identifier },
  }),
  onAPISenderRegister: (api, sender) => ({
    type: constants.API_SENDER_REGISTER,
    payload: { api, sender },
  }),
  onAPISenderSetValue: (api, sender, value) => ({
    type: constants.API_SENDER_SET_VALUE,
    payload: { api, sender, value },
  }),
};

export default withAPIActionCreators;
