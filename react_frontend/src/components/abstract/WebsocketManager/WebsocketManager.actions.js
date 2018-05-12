
import constants from 'store/constants';

const websocketManagerActionCreators = {
  openWebsocket: (socket, target) => ({
    type: constants.WEBSOCKET_OPEN,
    payload: { socket, target },
  }),
  closeWebsocket: socket => ({
    type: constants.WEBSOCKET_CLOSE,
    payload: { socket },
  }),
};

export default websocketManagerActionCreators;
