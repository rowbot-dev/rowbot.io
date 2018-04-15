
import { compose } from 'redux';
import { connect } from 'react-redux';

import WebsocketController from './WebsocketController'
import websocketControllerActionCreators from './actions';

const mapStateToProps = (state, props) => ({

});

const mapDispatchToProps = {
  onOpenWebsocket: websocketControllerActionCreators.openWebsocket,
  onSendWebsocketMessage: websocketControllerActionCreators.sendWebsocketMessage,
  onReceiveWebsocketMessage: websocketControllerActionCreators.receiveWebsocketMessage,
  onCloseWebsocket: websocketControllerActionCreators.closeWebsocket,
  onWebsocketError: websocketControllerActionCreators.websocketError,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(WebsocketController);
