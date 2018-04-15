
import constants from 'store/constants';

const websocketControllerReducer = (state={}, action) => {
  switch (action.type) {
    case constants.WEBSOCKET_CONNECT:
    case constants.WEBSOCKET_CONNECT_SUCCESS:
    case constants.WEBSOCKET_CONNECT_FAILURE:
    case constants.WEBSOCKET_SEND:
    case constants.WEBSOCKET_SEND_SUCCESS:
    case constants.WEBSOCKET_SEND_FAILURE:
    case constants.WEBSOCKET_RECEIVE:
    case constants.WEBSOCKET_RECEIVE_SUCCESS:
    case constants.WEBSOCKET_RECEIVE_FAILURE:
    default:
      return state;
  }
}

export default websocketControllerReducer;
