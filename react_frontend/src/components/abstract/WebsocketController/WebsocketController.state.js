
import { compose } from 'redux';
import { connect } from 'react-redux';

import WebsocketController from './WebsocketController'
import websocketControllerActionCreators from './actions';

const mapStateToProps = state => ({

});

const mapDispatchToProps = {
  onConnectToWebsocket: websocketControllerActionCreators.connectToWebsocket,
  onSendWebsocketMessage: websocketControllerActionCreators.sendWebsocketMessage,
  onReceiveWebsocketMessage: websocketControllerActionCreators.receiveWebsocketMessage,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(WebsocketController);
