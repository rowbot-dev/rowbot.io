
import constants from 'store/constants';

const websocketControllerReducer = (state={}, action) => {
  switch (action.type) {
    case constants.WEBSOCKET_OPEN:
    case constants.WEBSOCKET_OPEN_SUCCESS:
    case constants.WEBSOCKET_OPEN_FAILURE:
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
